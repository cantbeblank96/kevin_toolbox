from kevin.developing.executor import Executor


def get_executor_ls_by_samples(factory, samples, chunk_step, need_to_generate, **kwargs):
    """
        通过调用 verification.Factory 中的 generate_by_samples() 函数，
            来根据 samples 生成一系列的执行器 get_executor_ls，
            每个执行器在被 get_executor_ls() 调用后都将返回一个数据集
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
        返回：
            executor_ls：            list of get_executor_ls that can generate dataset by using get_executor_ls()
            size_ls：                产生的数据集的预期大小
    """
    executor_ls, size_ls = [], []
    #
    len_ = len(samples)
    count = 0
    while count < len_:
        # step
        step = min(chunk_step, len_ - count)
        # 计算
        executor_ls.append(Executor(func=factory.generate_by_samples,
                                    f_kwargs=dict(samples=Executor(func=samples.read, args=[count, count + step]),
                                                  need_to_generate=lambda: need_to_generate),
                                    kwargs=kwargs))
        size_ls.append(step)
        #
        count += step

    # 综合而言，
    #     除最后一个dataset以外，都有
    #     dataset_size = chunk_step
    #     最后一个dataset可能是残缺的，有
    #     0 < dataset_size <= dataset_size
    return executor_ls, size_ls
