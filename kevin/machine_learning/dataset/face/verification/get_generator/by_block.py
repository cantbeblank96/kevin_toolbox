import numpy as np
from kevin.machine_learning.dataset.face.verification import Factory
from kevin.machine_learning.dataset.face.verification.get_executor_ls import get_executor_ls_by_block_of_triangle, \
    get_executor_ls_by_block_of_all


def get_generator_by_block(**kwargs):
    """
        构造一个迭代生成数据集的迭代器，并返回
            （本函数主要基于 get_executor_ls_by_block_of_xxx() 进行实现，
            并为其输入参数添加了类型检查）
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
        executor_ls, size_ls = get_executor_ls_by_block_of_all(**paras)
    else:
        executor_ls, size_ls = get_executor_ls_by_block_of_triangle(**paras)
    generator = (executor() for executor in executor_ls)
    return generator


def cal_chunk_step(upper_bound):
    """
        根据数据集大小的限制，计算每个数据块的边长上界。
        返回值满足:
            chunk_step = argmax( chunk_step * (chunk_step + 1) <= upper_bound )
    """
    # block的宽
    return int(((1 + 4 * upper_bound) ** 0.5 - 1) / 2)
