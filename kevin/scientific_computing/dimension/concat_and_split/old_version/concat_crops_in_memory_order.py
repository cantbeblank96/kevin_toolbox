import numpy as np

from kevin.scientific_computing import utils
from kevin.patches.for_test import check_consistency

"""
旧版本的concat
不依赖树结构
"""


def concat_crops_in_memory_order(**kwargs):
    """
        将 crop 按照对应的 box 指示的位置，以行优先的内存顺序，进行拼接、展平

        参数：
            crop_ls:        <list of np.array/tensor>
            box_ls:         <list of np.arrays>
                                each element is an array with shape [2, dimensions]
                                各个维度的意义为：
                                    2：          box 的两个轴对称点
                                    dimensions： 坐标的维度
                                要求：
                                    - 各个 box 应该是已经 sorted 的（如果坐标未排序，则需要通过令 need_to_sort_box=True），
                                    - 各个 box 在坐标轴上的投影之间没有重叠部分
                                    函数 geometry.for_boxes.boolean_algebra() 返回的 boxes 结果，以及
                                    函数 geometry.for_boxes.detect_collision() 返回的 node_ls 中每个 node 下面
                                    的 node.description["by_boxes"] 都符合该要求。
            beg_axis:       <integer> 上面提供的 box 中指定的坐标是从 crop 的第几个 axis 开始对应的。
                                例如： beg_axis=1 时，box=[[i,j],[m,n]] 表示该 crop 是从原张量的 [:, i:m, j:n, ...] 部分截取出来的。
            need_to_sort_box:   <boolean> 对 box 的两个轴对称点的坐标进行排序。
                                例如 box=[[1,2],[0,4]] 在排序后将变为 [[0,2],[1,4]]
                                默认为 True，
                                如果可以确保输入的 box 都是已经排序好的，则可以令该参数为 False 以节省计算量。
            return_details: <boolean> 是否以详细信息的形式返回结果
                                默认为 False，此时返回：
                                    concat_result:  <np.array/tensor> 对 crop_ls 进行合并后的结果
                                当设置为 True，将返回一个 dict：
                                    details = dict(
                                        concat = <np.array/tensor>,  # 对 crop_ls 进行合并后的结果
                                        box_ls = <list of np.arrays>,  # 按照 内存顺序 对 box_ls 进行排序后的结果
                                        crop_ls = <list of np.array/tensor>,  # 按照 内存顺序 对 crop_ls 进行排序后的结果
                                        beg_axis = beg_axis,  # 对应与输入的 beg_axis
                                    )
        返回：
            concat_result 或者 details
    """
    # 默认参数
    paras = {
        # 必要参数
        "crop_ls": None,
        "box_ls": None,
        #
        "beg_axis": 0,
        "need_to_sort_box": False,
        "return_details": False,
    }

    # 获取参数
    paras.update(kwargs)

    # 校验参数
    assert isinstance(paras["crop_ls"], (list,)) and len(paras["crop_ls"]) > 0
    crop_ls = paras["crop_ls"]
    #
    _, function_table = utils.get_function_table_for_array_and_tensor(crop_ls[0])
    concat, flatten = function_table["concat"], function_table["flatten"]
    #
    if paras["need_to_sort_box"]:
        paras["box_ls"] = list(np.sort(np.asarray(paras["box_ls"]), axis=1))
    assert isinstance(paras["box_ls"], (list,)) and len(paras["box_ls"]) == len(paras["crop_ls"])
    assert paras["box_ls"][0].ndim == 2 and paras["box_ls"][0].shape[1] == 2
    box_ls = paras["box_ls"]
    #
    assert isinstance(paras["beg_axis"], (int,))
    beg_axis = paras["beg_axis"]
    end_axis = beg_axis + box_ls[0].shape[-1] - 1
    assert 0 <= beg_axis <= end_axis < crop_ls[0].ndim

    # 按行优先进行多级排序
    temp = sorted(zip(box_ls, crop_ls), key=lambda x: x[0][0].tolist())
    sorted_crop_ls = [crop for _, crop in temp]
    sorted_box_ls = [box for box, _ in temp]

    # 对 crop_ls 中的各个 crop 进行分组 concat 和展平
    crop_ls = sorted_crop_ls.copy()
    group = []  # 将能够合并的 crop 作为一组，寄存在 group 中
    # 循环次数上限：
    #   - 在每一轮中（end_axis位置相同的视为同一轮），每合并n个crop最多需要循环n次。
    #   - 最多有 end_axis-beg_axis+1 轮循环
    loop_limit = (end_axis - beg_axis + 1) * len(crop_ls)
    while len(crop_ls) + len(group) > 1 and loop_limit > 0:
        if len(group) == 0:
            group.append(crop_ls.pop(0))

        if len(crop_ls) > 0 and group[0].ndim == crop_ls[0].ndim and \
                group[0].shape[beg_axis:end_axis] == crop_ls[0].shape[beg_axis:end_axis]:
            # crop_ls[0] 与 group 中的元素具备进行 concat 的条件，是同一组，则添加到 group 中
            group.append(crop_ls.pop(0))
        else:
            # 不是同一组或者 crop_ls 已清空，则开始对 group 中的张量进行 concat
            res = concat(group, axis=end_axis)
            if beg_axis < end_axis:
                # 将已 concat 的部分进行展平，展平后的 ndim 将减1
                res = flatten(res, axis_0=end_axis - 1, axis_1=end_axis)
            # crop_ls[0] 与 group 中的元素不是同一组的情况有两种：
            #   1.crop_ls[0] 与 group[0] 的 ndim 不同。证明将要开启下一轮的分组和 concat。end_axis 需要向前移动。
            #   2.crop_ls[0] 与 group[0] 的 ndim 相同，但是 shape[start_axis:end_axis] 部分不同，证明还没有到下一轮。end_axis 不动。
            if len(crop_ls) > 0 and group[0].ndim != crop_ls[0].ndim:
                end_axis -= 1
            # 将 concat 结果添加回待处理队列的尾部，留给下一轮处理
            crop_ls.append(res)
            group = []

        loop_limit -= 1

    assert len(crop_ls) == 1, \
        f"crop_ls 中存在无法合并的项，请检查 box_ls 和 crop_ls 是否符合要求"
    res = crop_ls[0]

    if paras["return_details"]:
        details = dict(
            concat=res,
            crop_ls=sorted_crop_ls,
            box_ls=sorted_box_ls,
            beg_axis=beg_axis,
        )
        return details
    else:
        return res


def get_region_by_boxes(x, box_ls, beg_axis):
    """
        将 boxes 选定的区域截取出来

        参数：
            x:              <np.array/tensor>
            boxes:          <3 axis np.array>
                                shape [batch_size, 2, dimensions]，各个维度的意义为：
                                    batch_size： 有多少个 box
                                    2：          box的两个轴对称点
                                    dimensions： 坐标的维度
            beg_axis:       <integer> 上面提供的 boxes 中指定的坐标是从 x/crop 的第几个 axis 开始对应的。
                                例如： beg_axis=1 时，box=[[i,j],[m,n]] 表示该 crop 是从原张量的 x[:, i:m, j:n, ...] 部分截取出来的。
        返回：
            crop_ls:        <list of np.array/tensor>
    """
    # 根据 box 从 x 中截取 crop
    crop_ls = [x[tuple(
        [slice(None, None)] * beg_axis + [slice(beg, end) for beg, end in zip(box[0], box[1])]
    )] for box in box_ls]

    return crop_ls


if __name__ == '__main__':
    import torch
    from line_profiler import LineProfiler

    x_shape = [3, 16, 16, ]
    x = torch.arange(np.prod(x_shape)).reshape(x_shape)

    boxes = np.array([
        [[0, 0],
         [4, 4]],
        [[0, 4],
         [4, 16]],
        [[4, 0],
         [16, 4]],
        [[4, 4],
         [16, 16]],
    ])

    box_ls = list(np.sort(boxes, axis=1))

    crop_ls = utils.get_crop_by_box(x=x, box_ls=box_ls, beg_axis=1)

    # res = concat_crops_in_memory_order(crop_ls=crop_ls, box_ls=list(boxes), beg_axis=1, return_details=True)

    lp = LineProfiler()
    # lp_wrapper = lp(concat_crops_in_memory_order)
    # res = lp_wrapper(crop_ls=crop_ls, box_ls=box_ls, beg_axis=1, return_details=True)
    # lp.print_stats()
    #
    # print(res["concat"].shape)
    # print(torch.max(torch.abs(res["concat"] - x.reshape(3, -1, ))))

    """
    与新版本对比耗时
    基本没有差别，太棒了！！
    """
    from kevin.scientific_computing.dimension.concat_and_split import concat_crops_into_whole

    # concat_crops_into_whole(crop_ls=crop_ls, box_ls=box_ls, beg_axis=1, return_details=True)
    lp_wrapper = lp(concat_crops_into_whole)
    res = lp_wrapper(crop_ls=crop_ls, box_ls=box_ls, beg_axis=1, return_details=True)
    lp.print_stats()
