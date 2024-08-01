import pytest
from kevin_toolbox.patches.for_test import check_consistency
import numpy as np
import torch

from kevin_toolbox.math.dimension import transpose


@pytest.mark.parametrize("x_shape, axis",
                         list(zip([[5, 6, 6], [100, 100, 100], [1, 1, 1, 1], [4, 4]],
                                  [-2, 2, 1, -1]))[:])
def test_transpose_inside_axis_and_get_inverse_index_ls(x_shape, axis):
    print("test inside_axis and get_inverse_index_ls")

    x_ls = [np.random.rand(*x_shape), torch.rand(*x_shape)]
    index_ls = np.random.permutation(x_shape[axis])
    # 同时测试对 np.array 和 torch.tensor 的兼容性
    for x in x_ls:
        y = transpose.inside_axis(x=x, axis=axis, index_ls=index_ls, reverse=False)
        x1 = transpose.inside_axis(x=y, axis=axis, index_ls=index_ls, reverse=True)
        check_consistency(x, x1)
