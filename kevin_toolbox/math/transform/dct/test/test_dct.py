import pytest
from kevin_toolbox.patches.for_test import check_consistency
import numpy as np
import torch

from kevin_toolbox.math.transform import dct
from test_data.data_all import trans_matrix_ls, shape_ls


@pytest.mark.parametrize("shape, expected",
                         zip(shape_ls + [[1, 1], [4, 2], [5, 15], [1000, 100]],
                             trans_matrix_ls + [None] * 4))
def test_generate_trans_matrix(shape, expected):
    print("test dct.generate_trans_matrix()")

    # 验证结果
    B = dct.generate_trans_matrix(shape=shape)
    assert list(B.shape) == shape
    if expected is not None:
        check_consistency(B, expected)
    # 验证两种设定参数模式是等效的
    B_ = dct.generate_trans_matrix(sampling_points_num=shape[0], basis_series_num=shape[1])
    check_consistency(B, B_)
    # 验证正交性
    if shape[1] <= shape[0]:
        for c0 in range(shape[1]):
            for c1 in range(c0, shape[1]):
                p = np.sum(B[..., c0] * B[..., c1])
                if c0 == c1:
                    # inner product of the same basis should be 1
                    check_consistency(p, 1)
                else:
                    # inner product of the different basis should be 0
                    check_consistency(p, 0)


@pytest.mark.parametrize("shape, last_n_dims",
                         [([4, 4], 2),
                          ([100, 200, 3, 4, 5], 3),
                          ([3, 3, 100, 3, 50], 4)])
def test_calculator(shape, last_n_dims):
    print("test dct.Calculator")

    # 基函数数量与采样点数量相等时，应该是无损转换
    calculator = dct.Calculator()
    a = torch.rand(shape, dtype=torch.float32)
    b = calculator(a, reverse=False, basis_series_num_ls=shape[-last_n_dims:])
    a1 = calculator(b, reverse=True, sampling_points_num_ls=shape[-last_n_dims:])
    check_consistency(a, a1, tolerance=1e-5)

    # 基函数数量小于采样点数量时，应该是不保留高频的有损转换
    basis_series_num_ls_for_low_frequency = []
    basis_series_num_ls_for_high_frequency = []
    for i in shape[-last_n_dims:]:
        if i <= 1:
            temp = [i, i]
        else:
            temp = sorted(np.random.choice(range(1, i + 1), size=2, replace=False))
        basis_series_num_ls_for_low_frequency.append(temp[0])
        basis_series_num_ls_for_high_frequency.append(temp[1])
    # 先保留低频
    a = torch.rand(shape)
    b = calculator(a, reverse=False, basis_series_num_ls=basis_series_num_ls_for_low_frequency)
    a1 = calculator(b, reverse=True, sampling_points_num_ls=shape[-last_n_dims:])
    # 再尝试保留高频
    b1 = calculator(a1, reverse=False, basis_series_num_ls=basis_series_num_ls_for_high_frequency)
    a2 = calculator(b1, reverse=True, sampling_points_num_ls=shape[-last_n_dims:])
    check_consistency(a2, a1, tolerance=1e-6)
