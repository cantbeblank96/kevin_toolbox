import numpy as np
from kevin.machine_learning.patch_for_numpy.axis_and_dim import transpose
from .generate_z_pattern_indices import generate_z_pattern_indices


def stack_along_z_pattern(**kwargs):
    """
        将 x 最后的一个维度，按照 shape 对应的 z_pattern_indices 进行堆叠
            实际上就是打平展开 flatten_along_z_pattern() 的逆向操作

        参数：
            x：              <nparray/tensor>
            shape：          <list/tuple of integers>
    """
    # 默认参数
    paras = {
        # 必要参数
        "x": None,
        "shape": None
    }

    # 获取参数
    paras.update(kwargs)

    # 校验参数
    assert paras["shape"] is not None
    x = paras["x"]
    assert isinstance(paras["shape"], (list, tuple,)) and np.prod(paras["shape"]) == x.shape[-1], \
        f'type {type(paras["shape"])} in [list, tuple] ? \n{np.prod(paras["shape"])} == {x.shape[-1]}？'
    shape = paras["shape"]

    # 获取转置的逆
    source = np.arange(0, np.prod(shape)).astype(dtype=np.int32).reshape(shape)
    indices = generate_z_pattern_indices(shape=shape, trans_to_zip_type=True)
    index_ls = list(source[indices].reshape(-1))
    r_index_ls = transpose.get_inverse_index_ls(index_ls)

    # 对最后的维度进行转置
    y = transpose.inside_axis(x=x, axis=-1, index_ls=r_index_ls)

    # reshape
    new_shape = list(y.shape)[:-1] + list(shape)
    y = y.reshape(new_shape)

    return y
