import pytest
import numpy as np
from kevin_toolbox.patches.for_numpy import random
from kevin_toolbox.patches.for_test import check_consistency


def test_get_rng():
    print("test random.get_rng()")

    # 使用默认的全局的随机器
    rng_0 = random.get_rng()
    rng_1 = random.get_rng()
    # 全局的随机器 id 是一致的
    check_consistency(id(rng_0), id(rng_1))
    # 但是不同批次生成的随机数据是不同的
    with pytest.raises(AssertionError):
        check_consistency(rng_0.normal(size=100), rng_1.normal(size=100))

    # 使用根据指定 seed 构造的随机器
    rng_0 = random.get_rng(seed=114)
    rng_1 = random.get_rng(seed=114)
    # id 是不一致的
    with pytest.raises(AssertionError):
        check_consistency(id(rng_0), id(rng_1))
    # 生成的随机随机是相同的
    check_consistency(rng_0.normal(size=100), rng_1.normal(size=100))


def test_truncated_normal():
    print("test random.truncated_normal()")

    mean = 2
    sigma = 3
    size = 10000
    low, high = -7, 4  # 截断边界

    # 比较两种方式生成的随机变量的分布是否与目标一致
    expected = np.random.normal(mean, sigma, int(size * 1.5))
    expected = np.histogram(expected, bins=7, range=(low, high), density=True)[0]
    # 方式1（hit_ratio_threshold=0）
    res_1 = random.truncated_normal(mean, sigma, low, high, size=size, hit_ratio_threshold=0)
    res_1 = np.histogram(res_1, bins=7, range=(low, high), density=True)[0]
    assert np.all((low <= res_1) * (res_1 <= high))
    # 方式2（hit_ratio_threshold=1.0）
    res_2 = random.truncated_normal(mean, sigma, low, high, size=size, hit_ratio_threshold=1.0)
    res_2 = np.histogram(res_2, bins=7, range=(low, high), density=True)[0]
    assert np.all((low <= res_2) * (res_2 <= high))
    #
    check_consistency(res_2, res_1, expected, tolerance=1e-2 * 5)


def test_truncated_multivariate_normal():
    print("test random.truncated_multivariate_normal()")

    mean = np.array([1, 2])
    cov = np.array([[1, 0.5],
                    [0.5, 1]])
    size = 5000
    low_radius, high_radius = 0.5, 1.5

    # 比较两种方式生成的随机变量的分布是否与目标一致
    expected = np.random.multivariate_normal(mean, cov, int(size * 5))
    A = np.linalg.cholesky(cov)
    AH = np.linalg.inv(A)
    raw = np.sum((AH @ (expected - mean[None, :]).T).T ** 2, axis=-1, keepdims=False) ** 0.5
    expected = expected[(raw >= low_radius) * (raw < high_radius)]
    # 方式1（hit_ratio_threshold=0）
    res_1 = random.truncated_multivariate_normal(mean, cov, low_radius, high_radius, size=size, hit_ratio_threshold=0)
    # 方式2（hit_ratio_threshold=1.0）
    res_2 = random.truncated_multivariate_normal(mean, cov, low_radius, high_radius, size=size, hit_ratio_threshold=1.0)

    #
    for i in range(len(mean)):
        # 比较各个维度的概率分布是否一致
        temp_ls = expected[:, i], res_1[:, i], res_2[:, i]
        range_ = (min([min(i) for i in temp_ls]), max([max(i) for i in temp_ls]))
        temp_ls = [np.histogram(i, bins=7, range=range_, density=True)[0] for i in temp_ls]
        check_consistency(*temp_ls, tolerance=1e-2 * 5)
