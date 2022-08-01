from kevin.scientific_computing.axis_and_dim import transpose
from kevin.scientific_computing import utils


def transpose_inside_axis(**kwargs):
    """
        将变量 x 的第 axis 个轴内的各个维度，按照 index_ls 的顺序进行重排/转置

        参数：
            x:          <np.array/torch.tensor>
            axis:       <integer>
                            默认为 -1
            index_ls:   <list> 格式具体参考 axis_and_dim.coordinates
            reverse:    <boolean>
                            默认为 False
                            当设置为 True 时进行转置的逆

        建议：
            - 首先将 x 中需要重排的 axis 转置到最后能够加速本函数的执行。
    """
    # 默认参数
    paras = {
        # 必要参数
        "x": None,
        "index_ls": None,
        #
        "axis": -1,
        "reverse": False,
    }

    # 获取参数
    paras.update(kwargs)

    # 校验参数
    _, function_table = utils.get_function_table_for_array_and_tensor(paras["x"])
    swapaxes = function_table["swapaxes"]
    x = paras["x"]
    #
    assert isinstance(paras["axis"], (int,)) and paras["axis"] < x.ndim
    axis = paras["axis"]
    #
    assert isinstance(paras["index_ls"], (list, tuple,)) and len(paras["index_ls"]) == x.shape[axis], \
        f'{len(paras["index_ls"])} == {x.shape[axis]}？'
    index_ls = paras["index_ls"]
    if paras["reverse"]:
        index_ls = transpose.get_inverse_index_ls(index_ls=index_ls)

    x = swapaxes(x, axis, -1)
    x = x[..., index_ls]
    y = swapaxes(x, axis, -1)
    return y
