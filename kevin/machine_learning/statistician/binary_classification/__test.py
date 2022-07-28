from kevin.machine_learning.statistician.binary_classification import cal_cfm, merge_cfm_ls, cal_cfm_iteratively_by_chunk, cal_tpr_and_fpr, \
    Accumulator_for_Cfm

if __name__ == '__main__':
    import numpy as np
    from kevin.data_flow.core.reader import UReader

    print("构造测试数据")
    # scores = np.asarray([0.7, 0.5, 0.6, 0.4, 0.1, 0.4, 0.3]).reshape((-1, 1))
    # labels = np.asarray([1, 0, 1, 1, 0, 0, 1]).reshape((-1, 1))
    scores = np.asarray([0.7, 0.5, 0.6, 0.4, 0.1, 0.4, 0.3]).reshape((-1, 1))
    labels = np.asarray([1, 1, 1, 1, 1, 1, 1]).reshape((-1, 1))

    print("计算混淆矩阵")

    res_ = cal_cfm(scores, labels, decimals_of_scores=3)
    print(f"cal confusion matrices\n {res_}")

    res_ = merge_cfm_ls([res_, res_, res_])
    print(f"merge confusion matrices\n {res_}")

    res_ = cal_cfm_iteratively_by_chunk(UReader(var=scores), UReader(var=labels), chunk_step=2)
    print(f"cal confusion matrices iteratively by chunk\n {res_}")

    print("计算指标")

    res_ = cal_tpr_and_fpr(res_)
    print(f"cal_tpr_and_fpr\n tpr_ls {res_['tpr_ls']}\n fpr_ls {res_['fpr_ls']}")

    print("累加计算器")

    accumulator_for_cfm = Accumulator_for_Cfm(decimals_of_scores=2)
    accumulator_for_cfm(scores, labels)
    accumulator_for_cfm(scores, labels, chunk_step=2)
    accumulator_for_cfm(UReader(var=scores), UReader(var=labels))
    res_ = accumulator_for_cfm.get()
    print(f"accumulator_for_cfm\n {res_}")
    accumulator_for_cfm.reset()
