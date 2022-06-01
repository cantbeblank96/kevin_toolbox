import numpy as np
from kevin.machine_learning.patch_for_numpy.axis_and_dim import convert


def convert_index_to_indices(index_ls, shape):
    """
        将 index_ls 格式的坐标列表转换为 indices_ls 格式
    """
    assert index_ls.size <= np.prod(shape)

    source = np.zeros(shape=shape)
    zip_indices = np.where(source >= 0)
    indices_ls = convert.zip_type_to_indices(zip_indices=zip_indices)
    indices_ls = indices_ls[index_ls]
    return indices_ls












