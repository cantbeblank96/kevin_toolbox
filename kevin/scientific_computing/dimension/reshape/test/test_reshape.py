import pytest
from kevin.patches.for_test import check_consistency
import numpy as np
import torch

from kevin.scientific_computing.dimension import coordinates, reshape


@pytest.mark.parametrize("x_shape, dim_num, pattern",
                         list(zip([[10, 3, 4, 4], [100, 100, 100], [1, 1, 1, 1], [4, 4]],
                                  [3, 2, 4, 2],
                                  ["z_pattern", "z_pattern", "shuffle_inside_block", "shuffle_inside_block"]))[:])
def test_flatten_and_unflatten(x_shape, dim_num, pattern):
    print("test flatten and unflatten")
    x_ls = [np.random.rand(*x_shape), torch.rand(*x_shape)]

    # 同时测试对 np.array 和 torch.tensor 的兼容性
    for x in x_ls:
        # flatten
        y = reshape.flatten(x=x, dim_num=dim_num,
                            generate_func=lambda shape: coordinates.generate(shape=shape, pattern=pattern,
                                                                             output_format="zip_indices",
                                                                             kwargs=dict(seed=114)))
        print(f"flatten : {x.shape} ==> {y.shape}")

        # unflatten
        x1 = reshape.unflatten(x=y, shape=x_shape[-dim_num:],
                               generate_func=lambda shape: coordinates.generate(shape=shape, pattern=pattern,
                                                                                output_format="index_ls",
                                                                                kwargs=dict(seed=114)))
        print(f"unflatten : {y.shape} ==> {x1.shape}")

        check_consistency(x1, x)


@pytest.mark.parametrize("x_shape, block_shape, expected_y_shape",
                         list(zip([[5, 6, 6], [100, 100, 100], [1, 1, 1, 1], [4, 4]],
                                  [[3, 2], [100, 100], [1, 1, 1], [2]],
                                  [[5, 2, 3, 3, 2], [100, 1, 1, 100, 100], [1, 1, 1, 1, 1, 1, 1], [4, 2, 2]]))[:])
def test_split_and_merge_blocks(x_shape, block_shape, expected_y_shape):
    print("test merge and split blocks")

    x_ls = [np.random.rand(*x_shape), torch.rand(*x_shape)]

    # 同时测试对 np.array 和 torch.tensor 的兼容性
    for x in x_ls:
        # split
        y = reshape.split_blocks(x=x, block_shape=block_shape)
        print(f"split : {x.shape} ==> {y.shape}")
        assert list(y.shape) == expected_y_shape

        # merge
        x1 = reshape.merge_blocks(x=y, block_axis_num=len(block_shape))
        print(f"merge : {y.shape} ==> {x1.shape}")

        check_consistency(x1, x)
