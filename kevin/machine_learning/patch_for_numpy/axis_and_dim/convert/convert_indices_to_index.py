import numpy as np
from kevin.machine_learning.patch_for_numpy.axis_and_dim import convert


def convert_indices_to_index(indices_ls, shape):
    """
        将 indices_ls 格式的坐标列表转换为 index_ls 格式
    """
    assert indices_ls.shape[1] == len(shape)

    source = np.arange(0, np.prod(shape)).astype(dtype=np.int32).reshape(shape)
    zip_indices = convert.indices_to_zip_type(indices_ls)
    index_ls = list(source[zip_indices].reshape(-1))
    return index_ls
