import numpy as np
from kevin.machine_learning.dataset.face.verification import Factory

"""数据集生成器"""


def get_generator_by_block(**kwargs):
    """
        构造一个迭代生成数据集的迭代器，并返回
        参数：
            mode:                   构造哪种迭代器，现在支持以下模式：
                                        "all":  使用 generator_by_block_of_all() 构造
                                        "triangle": 使用 generator_by_block_of_triangle() 构造
        其他参数：
            factory:                verification.Factory 实例
            chunk_step:             每个分块的大小（根据实际内存容量来选择）
                                        限制了每次返回的数据集大小。
            upper_bound_of_dataset_size:        每次返回的数据集的大小的上界（根据实际内存容量来选择）
                                        当给定有 upper_bound_of_dataset_size 时，程序将可以通过 cal_chunk_step() 来计算得到 chunk_step。
                                        该参数是间接设置 chunk_step 的方式，但相较而言更加直观。
            （建议使用 upper_bound_of_dataset_size 而不使用 chunk_step。两者同时设置时，将以两者中最小的为限制）
            need_to_generate:       需要生成的字段
                                        （参见 Factory.generate_by_block() 中的介绍）
            include_diagonal:       是否包含对角线
    """
    # 默认参数
    paras = {
        "mode": "triangle",
        "factory": None,
        "chunk_step": None,
        "upper_bound_of_dataset_size": None,
        "need_to_generate": None,
        "include_diagonal": True,
    }

    # 获取参数
    paras.update(kwargs)

    # 校验参数
    assert paras["mode"] in ["all", "triangle"]
    assert isinstance(paras["factory"], (Factory,)), \
        Exception(f"Error: The type of input factory should be {Factory}, but get a {type(paras['factory'])}!")

    chunk_step_ls = []
    if paras["upper_bound_of_dataset_size"] is not None:
        chunk_step_ls.append(cal_chunk_step(paras["upper_bound_of_dataset_size"]))
    if paras["chunk_step"] is not None:
        chunk_step_ls.append(paras["chunk_step"])
    assert len(chunk_step_ls) > 0
    paras["chunk_step"] = min(chunk_step_ls)

    #
    if paras["mode"] == "all":
        return generator_by_block_of_all(**paras)
    else:
        return generator_by_block_of_triangle(**paras)


def cal_chunk_step(upper_bound):
    """
        根据数据集大小的限制，计算每个数据块的边长上界。
        返回值满足:
            chunk_step = argmax( chunk_step * (chunk_step + 1) <= upper_bound )
    """
    # block的宽
    return int(((1 + 4 * upper_bound) ** 0.5 - 1) / 2)


def generator_by_block_of_all(factory, chunk_step, need_to_generate, **kwargs):
    """
        通过调用 verification.Factory 中的 generate_by_block() 函数，来对整个矩阵，迭代生成数据集
        参数：
            factory:                verification.Factory 实例
            chunk_step:             每个分块的大小
            need_to_generate:       需要生成的字段
                                        （参见 Factory.generate_by_block() 中的介绍）
    """

    width = len(factory.paras["features"])  # 矩阵的宽度
    assert width > 0, \
        Exception("Error: the length of features in the input factory should be larger than 0!")

    # block的数量
    chunk_nums = (width - 1) // chunk_step + 1

    """
    迭代生成数据集
    """
    # 对于完整的 block（去除最后一行、列上的block）
    #     将整个block作为一个dataset
    #     dataset_size = chunk_step * chunk_step
    for i in range(chunk_nums - 1):
        i_0 = i * chunk_step
        i_1 = i_0 + chunk_step
        for j in range(chunk_nums - 1):
            j_0 = j * chunk_step
            j_1 = j_0 + chunk_step
            # 计算
            res = factory.generate_by_block(i_0, i_1, j_0, j_1,
                                            pick_triangle=False,
                                            need_to_generate=need_to_generate)
            yield res

    # 对于最后一行
    #     对于完整的矩形有
    #     chunk_step * chunk_step < dataset_size <= chunk_step * (chunk_step + 1)
    # 注意：
    #     对于最后一个可能残缺的矩阵（亦即大小不满足下界），
    #     该部分将与接下来的最后一列的部分头部组成一个dataset
    size_lower = chunk_step * chunk_step
    size_upper = chunk_step * (chunk_step + 1)
    res = None
    for res in __generator_by_block_along_axis(factory,
                                               i_0=(chunk_nums - 1) * chunk_step,
                                               i_1=width,
                                               j_0=0,
                                               j_1=width,
                                               axis_to_split="j", size_upper=size_upper,
                                               need_to_generate=need_to_generate, pre_res=res):
        if len(res[list(need_to_generate)[0]]) > size_lower:
            yield res
            res = None

    # 对于最后一列
    #     第一个矩形将与前面残缺的部分整合为一个dataset，该矩形的行数将根据缺少部分的数量计算得到，从而保证
    #     chunk_step * chunk_step <= dataset_size <= chunk_step * (chunk_step + 1)
    #     接下来的矩形将调整行数以尽量贴近上界，
    #     对于完整的矩形有
    #     chunk_step * chunk_step < dataset_size <= chunk_step * (chunk_step + 1)
    #     对于最后一个可能残缺的矩阵，有
    #     dataset_size <= chunk_step * (chunk_step + 1)
    # 这里承接上面的  res
    if chunk_nums > 1:
        yield from __generator_by_block_along_axis(factory,
                                                   i_0=0,
                                                   i_1=(chunk_nums - 1) * chunk_step,
                                                   j_0=(chunk_nums - 1) * chunk_step,
                                                   j_1=width,
                                                   axis_to_split="i", size_upper=size_upper,
                                                   need_to_generate=need_to_generate, pre_res=res)
    elif res is not None:
        yield res

    # 综合而言，
    #     除最后一个dataset以外，都有
    #     chunk_step * chunk_step <= dataset_size <= chunk_step * (chunk_step + 1)
    #     最后一个dataset可能是残缺的，有
    #     0 < dataset_size <= chunk_step * (chunk_step + 1)


def generator_by_block_of_triangle(factory, chunk_step, need_to_generate, include_diagonal=True, **kwargs):
    """
        通过调用 verification.Factory 中的 generate_by_block() 函数，来对矩阵的上三角部分，迭代生成数据集
        参数：
            factory:                verification.Factory 实例
            chunk_step:             每个分块的大小
            need_to_generate:       需要生成的字段
                                        （参见 Factory.generate_by_block() 中的介绍）
            include_diagonal:       是否包含对角线
    """

    width = len(factory.paras["features"])  # 矩阵的宽度
    assert width > 0, \
        Exception("Error: the length of features in the input factory should be larger than 0!")

    if include_diagonal:
        offset = 0
    else:
        # 如果要除去对角线，相当于去掉矩阵的第0列和最后一行
        # 宽度减1
        width -= 1
        # 在迭代时还需要为坐标添加一个偏置
        offset = 1

    # block的数量
    chunk_nums = (width - 1) // chunk_step + 1

    """
    迭代生成数据集
    """
    # 对于完整的 block（去除对角上、和最后一列上的block）
    #     将整个block作为一个dataset
    #     dataset_size = chunk_step * chunk_step
    for i in range(chunk_nums - 1):
        i_0 = i * chunk_step
        i_1 = i_0 + chunk_step
        for j in range(i + 1, chunk_nums - 1):
            j_0 = j * chunk_step + offset
            j_1 = j_0 + chunk_step
            # 计算
            res = factory.generate_by_block(i_0, i_1, j_0, j_1,
                                            pick_triangle=False,
                                            need_to_generate=need_to_generate)
            yield res

    # 对于对角线上的半个 block
    #     将两个上三角拼凑为一个dataset
    #     dataset_size = chunk_step * (chunk_step + 1)
    # 注意：
    #     当上三角的数量是奇数或者最后一个三角是残缺的话，
    #     该部分将与接下来的最后一列的部分头部组成一个dataset
    size_upper = chunk_step * (chunk_step + 1)
    res = None
    for res in __generator_by_block_along_diagonal(factory,
                                                   i_0=0,
                                                   i_1=width,
                                                   j_0=offset,
                                                   j_1=width + offset,
                                                   chunk_step=chunk_step,
                                                   need_to_generate=need_to_generate,
                                                   pick_triangle=True, include_diagonal=True):
        if len(res[list(need_to_generate)[0]]) == size_upper:
            yield res
            res = None

    # 对于最后一列
    #     第一个矩形将与前面残缺的上三角整合为一个dataset，该矩形的行数将根据缺少部分的数量计算得到，从而保证
    #     chunk_step * chunk_step <= dataset_size <= chunk_step * (chunk_step + 1)
    #     接下来的矩形将调整行数以尽量贴近上界，
    #     对于完整的矩形有
    #     chunk_step * chunk_step < dataset_size <= chunk_step * (chunk_step + 1)
    #     对于最后一个可能残缺的矩阵，有
    #     dataset_size <= chunk_step * (chunk_step + 1)
    # 这里承接上面的  res
    if chunk_nums > 1:
        yield from __generator_by_block_along_axis(factory,
                                                   i_0=0,
                                                   i_1=(chunk_nums - 1) * chunk_step,
                                                   j_0=(chunk_nums - 1) * chunk_step + offset,
                                                   j_1=width + offset,
                                                   axis_to_split="i", size_upper=size_upper,
                                                   need_to_generate=need_to_generate, pre_res=res)
    elif res is not None:
        yield res

    # 综合而言，
    #     除最后一个dataset以外，都有
    #     chunk_step * chunk_step <= dataset_size <= chunk_step * (chunk_step + 1)
    #     最后一个dataset可能是残缺的，有
    #     0 < dataset_size <= chunk_step * (chunk_step + 1)


def __generator_by_block_along_axis(factory, i_0, i_1, j_0, j_1, axis_to_split, size_upper, need_to_generate,
                                    pre_res=None):
    """
        通过调用 verification.Factory 中的 generate_by_block() 函数，来在（i_0, i_1, j_0, j_1）指定的子矩阵范围内，
            沿着 axis 指定的轴线方向，以 size_upper 为目标大小进行分割，迭代生成数据集
        参数：
            factory:                verification.Factory 实例
            i_0, i_1, j_0, j_1:     子矩阵的范围
                                        （支持多种方式输入，具体参见 Factory.generate_by_block() 中的介绍）
            axis_to_split:          分割子矩阵的方向
                                        可选值： ["i", "j"]
                                        以 "i" 为例，此时子矩阵沿行分割为 [i_0, i_0+step, ... ,i_1]
            size_upper:             每个分块的目标大小（大小的上界）
            pre_res:                前置的数据集
                                        第一个chunk产生的数据集将与pre_res整合为一个dataset并返回
            need_to_generate:       需要生成的字段
                                        （参见 Factory.generate_by_block() 中的介绍）

        关于返回的数据集大小（以axis="i"为例，令j_len:=j_1-j_0）：
            当 pre_res=None 时，
                对于前面完整的矩形，该矩形的行数将根据与size_upper相差的部分的数量计算得到，
                从而保证合并后返回的数据集尽量贴近上界，有
                dataset_size = size_upper//j_len * j_len
                对于最后一个残缺的矩形，有
                dataset_size <= size_upper
            当 pre_res 有值时，
                第一个矩形将与pre_res整合为一个dataset，有
                dataset_size <= min( size_upper//j_len * j_len, len(pre_res) )
                其他同上。
    """
    assert axis_to_split in ["i", "j"]
    i_len = i_1 - i_0 if isinstance(i_0, (int,)) else len(i_0)
    j_len = j_1 - j_0 if isinstance(j_0, (int,)) else len(j_0)
    assert i_len > 0 and j_len > 0
    len_fix, len_to_split = (j_len, i_len) if axis_to_split == "i" else (i_len, j_len)

    #
    count = 0
    while count < len_to_split:
        # step
        if count == 0 and pre_res is not None:
            # 对于第一个矩形
            pre_size = len(pre_res[list(need_to_generate)[0]])
            step = (size_upper - pre_size) // len_fix
            if step <= 0:  # pre_size 已经可以直接返回了
                yield pre_res
                pre_res = None
                continue
        else:
            step = size_upper // len_fix
        step = min(step, len_to_split - count)

        # 范围
        if axis_to_split == "i":
            i_0_, i_1_ = count, count + step
            if not isinstance(i_0, (int,)):
                i_0_, i_1_ = i_0[i_0_:i_1_], None
            j_0_, j_1_ = j_0, j_1
        else:
            j_0_, j_1_ = count, count + step
            if not isinstance(j_0, (int,)):
                j_0_, j_1_ = j_0[j_0_:j_1_], None
            i_0_, i_1_ = i_0, i_1

        # 计算
        res = factory.generate_by_block(i_0_, i_1_, j_0_, j_1_,
                                        pick_triangle=False,
                                        need_to_generate=need_to_generate)

        # 对于第一个矩形，进行合并
        if count == 0 and pre_res is not None:
            for key in need_to_generate:
                res[key] = np.concatenate((pre_res[key], res[key]), axis=0)

        #
        count += step

        # 返回
        yield res


def __generator_by_block_along_diagonal(factory, i_0, i_1, j_0, j_1, chunk_step, need_to_generate,
                                        pick_triangle=True, include_diagonal=True):
    """
        通过调用 verification.Factory 中的 generate_by_block() 函数，来在（i_0, i_1, j_0, j_1）指定的子矩阵范围内，
            沿着 对角线，以 chunk_step 为间隔迭代生成数据集
        参数：
            factory:                verification.Factory 实例
            i_0, i_1, j_0, j_1:     子矩阵的范围
                                        （支持多种方式输入，具体参见 Factory.generate_by_block() 中的介绍）
            chunk_step:             chunk的长宽
            pre_res:                前置的数据集
                                        第一个chunk产生的数据集将与pre_res整合为一个dataset并返回
            need_to_generate:       需要生成的字段
                                        （参见 Factory.generate_by_block() 中的介绍）
            pick_triangle:          只取block的上三角
            include_diagonal:       是否包含对角线

        关于返回的数据集大小：
            当 pick_triangle=True 时，
            只取上三角
                将每两个 chunk 矩形的上三角，将两个上三角拼凑为一个dataset，有
                    dataset_size = chunk_step * (chunk_step + offset)
                    其中，当包含对角线上元素时，offset=1，不包含则为-1。
                当上三角的数量是奇数或者最后一个三角是残缺的话，
                    对于最后一个残缺的数据集，有
                    dataset_size <= chunk_step * (chunk_step + offset)
            当 pick_triangle=False 时，
            取整个block
                此时对于完整的矩形，有
                    dataset_size = chunk_step * chunk_step
                对于最后一个残缺的矩形，有
                    dataset_size <= chunk_step * chunk_step
    """
    i_len = i_1 - i_0 if isinstance(i_0, (int,)) else len(i_0)
    j_len = j_1 - j_0 if isinstance(j_0, (int,)) else len(j_0)
    assert 0 < i_len == j_len

    size_lower = chunk_step * (chunk_step + 1) if pick_triangle else chunk_step * (chunk_step - 1)
    size = 0
    res = None
    count = 0
    while count < i_len:
        # 范围
        step = min(i_len - count, chunk_step)

        # 计算
        tmp = factory.generate_by_block(i_0=i_0 + count, i_1=i_0 + count + step,
                                        j_0=j_0 + count, j_1=j_0 + count + step,
                                        pick_triangle=pick_triangle,
                                        include_diagonal=include_diagonal,
                                        need_to_generate=need_to_generate)
        tmp_size = len(tmp[list(need_to_generate)[0]])

        #
        if size == 0:
            res, size = tmp, tmp_size
        else:
            # 合并
            size += tmp_size
            for key in need_to_generate:
                res[key] = np.concatenate((res[key], tmp[key]), axis=0)
        #
        count += step

        # 返回
        if size >= size_lower:
            size = 0
            yield res

    # 最后一个
    if size > 0:
        yield res
