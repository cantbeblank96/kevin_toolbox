import pytest
import numpy as np
import torch
from privacy_face.transform import dct
from privacy_face.transform.dct.test_data.data_all import trans_matrix_ls, shape_ls


@pytest.mark.parametrize("r_num, c_num",
                         zip([1, 4, 5, 1000], [1, 2, 15, 100]))
def test_generate_trans_matrix__part_0(r_num, c_num):
    print("test dct.generate_trans_matrix() part_0")

    B = dct.generate_trans_matrix(shape=[r_num, c_num])
    B_ = dct.generate_trans_matrix(sampling_points_num=r_num, basis_series_num=c_num)
    # 验证两种设定参数模式是等效的
    assert list(B.shape) == [r_num, c_num] and np.max(np.abs(B - B_)) < 1e-7
    # 验证正交性
    if c_num <= r_num:
        for c0 in range(c_num):
            for c1 in range(c0, c_num):
                p = np.sum(B[..., c0] * B[..., c1])
                if c0 == c1:
                    # inner product of the same basis should be 1
                    assert np.abs(p - 1) < 1e-7
                else:
                    # inner product of the different basis should be 0
                    assert np.abs(p) < 1e-7


@pytest.mark.parametrize("shape, expected",
                         zip(shape_ls, trans_matrix_ls))
def test_generate_trans_matrix__part_1(shape, expected):
    print("test dct.generate_trans_matrix() part_1")

    B = dct.generate_trans_matrix(shape=shape)
    assert list(B.shape) == shape and np.max(np.abs(B - expected)) < 1e-7


@pytest.mark.parametrize("shape, last_n_dims",
                         [([4, 4], 2),
                          ([100, 200, 3, 4, 5], 3),
                          ([3, 3, 100, 3, 50], 4)])
def test_calculator__part_0(shape, last_n_dims):
    # 基函数数量与采样点数量相等时，应该是无损转换
    calculator = dct.Calculator()
    a = torch.rand(shape)
    b = calculator(a, reverse=False, basis_series_num_ls=shape[-last_n_dims:])
    a1 = calculator(b, reverse=True, sampling_points_num_ls=shape[-last_n_dims:])
    assert torch.max(torch.abs(a.to(a1.device) - a1)) < 1e-5

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
    assert torch.max(torch.abs(a2.to(a1.device) - a1)) < 1e-5
