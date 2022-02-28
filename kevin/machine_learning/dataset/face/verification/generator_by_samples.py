from kevin.machine_learning.dataset.face.verification import Factory
from kevin.data_flow.reader import Unified_Reader_Base

"""数据集生成器"""


def get_generator_by_samples(**kwargs):
    """
        构造一个迭代生成数据集的迭代器，并返回
        参数：
            samples:                list of feature_id pairs
                                        np.array with dtype=np.int
                                        shape [sample_nums, 2]
                                        需要被 Unified_Reader_Base 包裹
        其他参数：
            factory:                verification.Factory 实例
            upper_bound_of_dataset_size/chunk_step:        每次返回的数据集的大小的上界（根据实际内存容量来选择）
            need_to_generate:       需要生成的字段
                                        （参见 Factory.generate_by_block() 中的介绍）
            feature_ids_is_sequential:       boolean，feature_ids 是否以1为间距递增的
                                        （参见 Factory.generate_by_samples() 中的介绍）
    """
    # 默认参数
    paras = {
        "samples": None,
        "factory": None,
        "chunk_step": None,
        "upper_bound_of_dataset_size": None,
        "need_to_generate": None,
    }

    # 获取参数
    paras.update(kwargs)

    # 校验参数
    chunk_step_ls = []
    if paras["upper_bound_of_dataset_size"] is not None:
        chunk_step_ls.append(paras["upper_bound_of_dataset_size"])
    if paras["chunk_step"] is not None:
        chunk_step_ls.append(paras["chunk_step"])
    assert len(chunk_step_ls) > 0
    paras["chunk_step"] = min(chunk_step_ls)
    #
    assert isinstance(paras["samples"], (Unified_Reader_Base,)), \
        Exception(
            f"Error: The type of input factory should be {Unified_Reader_Base}, but get a {type(paras['samples'])}!")
    assert isinstance(paras["factory"], (Factory,)), \
        Exception(f"Error: The type of input factory should be {Factory}, but get a {type(paras['factory'])}!")

    return generator_by_samples(**paras)


def generator_by_samples(factory, samples, chunk_step, need_to_generate, **kwargs):
    """
        通过调用 verification.Factory 中的 generate_by_samples() 函数，来根据 samples 迭代生成数据集
        参数：
            factory:                verification.Factory 实例
            samples:                list of feature_id pairs
                                        np.array with dtype=np.int
                                        shape [sample_nums, 2]
                                        需要被 Unified_Reader_Base 包裹
            chunk_step:             每个分块的大小
            need_to_generate:       需要生成的字段
                                        （参见 Factory.generate_by_samples() 中的介绍）
            feature_ids_is_sequential:       boolean，feature_ids 是否以1为间距递增的
                                        （参见 Factory.generate_by_samples() 中的介绍）
    """

    #
    len_ = len(samples)
    count = 0
    while count < len_:
        # step
        step = min(chunk_step, len_ - count)
        # 计算
        res = factory.generate_by_samples(samples.read(count, count + step),
                                          need_to_generate=need_to_generate, **kwargs)
        #
        count += step
        # 返回
        yield res

    # 综合而言，
    #     除最后一个dataset以外，都有
    #     dataset_size = chunk_step
    #     最后一个dataset可能是残缺的，有
    #     0 < dataset_size <= dataset_size
