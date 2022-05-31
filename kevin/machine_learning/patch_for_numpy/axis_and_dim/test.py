import os
import sys
import numpy as np

import z_pattern, transpose

if __name__ == '__main__':
    print("test transpose")

    print("inside_axis and get_inverse_index_ls")
    x = np.random.rand(*[10, 3, 4, 4])  # np.array([0, 1, 2, 3]).reshape(-1, 1)
    index_ls = [2, 0, 3, 1]
    y1 = transpose.inside_axis(x=x, axis=-2, index_ls=index_ls)
    y2 = transpose.inside_axis(x=y1, axis=-2, index_ls=transpose.get_inverse_index_ls(index_ls))
    print(f"deviation : {np.max(x - y2)}")

    print("test z_pattern")
    print("generate_indices")
    shape = (3, 4, 4)
    indices = z_pattern.generate_indices(shape=shape, trans_to_zip_type=True)
    print(indices)
    print(np.ones(shape=(3, 4, 4, 10))[indices].shape)

    print("flatten and stack")
    x = np.arange(0, np.prod(shape)).astype(dtype=np.int32).reshape(shape)  # np.random.rand(*[10, 3, 4, 4])
    y = z_pattern.flatten(x=x, dim_num=3)
    print(f"flatten : {x.shape} ==> {y.shape}")
    x1 = z_pattern.stack(x=y, shape=shape)
    print(f"stack : {y.shape} ==> {x1.shape}")
    print(f"deviation : {np.max(x1 - x)}")
