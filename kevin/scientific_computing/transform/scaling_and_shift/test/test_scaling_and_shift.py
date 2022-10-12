import pytest
from kevin.patches.for_test import check_consistency
import numpy as np
import torch

from kevin.scientific_computing.transform import scaling_and_shift


@pytest.mark.parametrize("x_shape, factor, zero_point",
                         list(zip([[5, 6, 6], [100, 100, 100], [1, 1, 1, 1], [4, 4]],
                                  [0.1, 1000, 1000, 0.01],
                                  [-2, 2, 1000, -1000]))[:])
def test_scaling(x_shape, factor, zero_point):
    print("test scaling")

    x_ls = [np.random.rand(*x_shape), torch.rand(*x_shape)]
    # 同时测试对 np.array 和 torch.tensor 的兼容性
    for x in x_ls:
        y = scaling_and_shift.scaling(x=x, factor=factor, zero_point=zero_point)  # 中心化
        x1 = scaling_and_shift.scaling(x=y, factor=factor, zero_point=zero_point, reverse=True)  # 去中心化
        check_consistency(x, x1, tolerance=1e-2)
