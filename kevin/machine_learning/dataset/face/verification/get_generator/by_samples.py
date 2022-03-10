from kevin.machine_learning.dataset.face.verification import Factory
from kevin.data_flow.reader import Unified_Reader_Base
from kevin.machine_learning.dataset.face.verification.get_executor_ls import get_executor_ls_by_samples


def get_generator_by_samples(**kwargs):
    """
        构造一个迭代生成数据集的迭代器，并返回
            （本函数主要基于 get_executor_ls_by_samples() 进行实现，
            并为其输入参数添加了类型检查）
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
    # samples
    assert isinstance(paras["samples"], (Unified_Reader_Base,)), \
        Exception(f"The type of input factory should be {Unified_Reader_Base}, but get a {type(paras['samples'])}!")
    # factory
    assert isinstance(paras["factory"], (Factory,)), \
        Exception(f"The type of input factory should be {Factory}, but get a {type(paras['factory'])}!")
    # chunk_step / upper_bound_of_dataset_size
    chunk_step_ls = []
    if paras["upper_bound_of_dataset_size"] is not None:
        chunk_step_ls.append(paras["upper_bound_of_dataset_size"])
    if paras["chunk_step"] is not None:
        chunk_step_ls.append(paras["chunk_step"])
    assert len(chunk_step_ls) > 0
    paras["chunk_step"] = min(chunk_step_ls)

    # 构建 get_generator
    executor_ls, size_ls = get_executor_ls_by_samples(**paras)
    generator = (executor() for executor in executor_ls)
    return generator
