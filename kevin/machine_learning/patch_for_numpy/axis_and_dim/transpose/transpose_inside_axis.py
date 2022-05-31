def transpose_inside_axis(x, axis, index_ls):
    """
        将变量 x 的第 axis 个轴内的各个维度，按照 index_ls 的顺序进行重排/转置
    """
    assert isinstance(index_ls, (list, tuple,)) and len(index_ls) == x.shape[axis], \
        f"{len(index_ls)} == {x.shape[axis]}？"

    x = x.swapaxes(axis, -1)
    y = x[..., index_ls]
    y = y.swapaxes(axis, -1)
    return y