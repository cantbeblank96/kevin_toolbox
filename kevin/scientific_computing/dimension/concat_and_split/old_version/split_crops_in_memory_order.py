"""
旧版本的split
存在致命的逻辑错误，已废弃
"""


def split_crops_in_memory_order(**kwargs):
    """
        将变量 x 按照 box_ls 指示的位置，以行优先的内存顺序，拆解成多个 crop
            系 concat_crops_in_memory_order() 的逆变换

        参数：
            x:              <np.array/tensor>
            box_ls:         <list of np.arrays>
                                each element is an array with shape [2, dimensions]
                                具体介绍参见 concat_crops_in_memory_order()
            beg_axis:       <integer> 要对 x 进行分割的轴
                                上面提供的 box 中指定的坐标是从 crop 的第 beg_axis 个 axis 开始对应的。
                                例如： beg_axis=1 时，box=[[i,j],[m,n]] 表示该 crop 是从原张量的 [:, i:m, j:n, ...] 部分截取出来的。
            need_to_sort_box:   <boolean> 对 box 的两个轴对称点的坐标进行排序。
            return_details: <boolean> 是否以详细信息的形式返回结果
                                默认为 False，此时返回：
                                    crop_ls:  <list of np.array/tensor> 分割结果
                                当设置为 True，将返回一个 dict：
                                    details = dict(
                                        crop_ls = <list of np.array/tensor>,  # 分割结果，而且是已经按照 内存顺序 进行排序后的结果
                                        concat = x,  # 对应于输入的 x
                                        box_ls = <list of np.arrays>,  # 按照 内存顺序 对 box_ls 进行排序后的结果
                                        beg_axis = beg_axis,  # 对应与输入的 beg_axis
                                    )
        返回：
            crop_ls 或者 details
    """
    # 默认参数
    paras = {
        # 必要参数
        "x": None,
        "box_ls": None,
        #
        "beg_axis": 0,
        "need_to_sort_box": False,
        "return_details": False,
    }

    # 获取参数
    paras.update(kwargs)

    # 校验参数
    assert paras["x"] is not None
    x = paras["x"]
    #
    if paras["need_to_sort_box"]:
        paras["box_ls"] = list(np.sort(np.asarray(paras["box_ls"]), axis=1))
    assert isinstance(paras["box_ls"], (list,)) and paras["box_ls"][0].ndim == 2 and paras["box_ls"][0].shape[1] == 2
    box_ls = paras["box_ls"]
    #
    assert isinstance(paras["beg_axis"], (int,)) and 0 <= paras["beg_axis"] < paras["x"].ndim
    beg_axis = paras["beg_axis"]

    # 按行优先进行多级排序
    sorted_box_ls = sorted(box_ls, key=lambda x: x[0].tolist())

    crop_ls = []
    beg = 0
    slice_for_x = [slice(None, None)] * (beg_axis + 1)
    for box in sorted_box_ls:
        end = beg + np.prod(box[1] - box[0])
        slice_for_x[-1] = slice(beg, end)
        new_shape = list(x.shape[:beg_axis]) + (box[1] - box[0]).tolist() + list(x.shape[beg_axis + 1:])
        crop_ls.append(x[tuple(slice_for_x)].reshape(new_shape))
        #
        beg = end

    if paras["return_details"]:
        details = dict(
            concat=x,
            crop_ls=crop_ls,
            box_ls=sorted_box_ls,
            beg_axis=beg_axis,
        )
        return details
    else:
        return crop_ls
