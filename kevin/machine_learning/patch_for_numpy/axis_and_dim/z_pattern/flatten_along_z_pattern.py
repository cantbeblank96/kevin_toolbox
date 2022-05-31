from .generate_z_pattern_indices import generate_z_pattern_indices


def flatten_along_z_pattern(**kwargs):
    """
        将 x 的最后 dim_num 个维度按照 z_pattern_indices 进行打平展开

        参数：
            x：              <nparray/tensor>
            dim_num：        <integer>
    """
    # 默认参数
    paras = {
        # 必要参数
        "x": None,
        "dim_num": True,
    }

    # 获取参数
    paras.update(kwargs)

    # 校验参数
    assert paras["x"] is not None
    x = paras["x"]
    assert isinstance(paras["dim_num"], (int,)) and 1 < paras["dim_num"] <= len(x.shape)
    dim_num = paras["dim_num"]

    # 首先将 y 要被展开的维度提前
    # y: [64, 8, 4] ==> [8, 4, 64]
    dim_ls = list(range(len(x.shape)))
    dim_ls = dim_ls[-dim_num:] + dim_ls[:-dim_num]
    y = x.transpose(*dim_ls)

    # 按照 z_pattern_indices 展开
    # y: [8, 4, 64] ==> [32, 64]
    indices = generate_z_pattern_indices(shape=x.shape[-dim_num:], trans_to_zip=True)
    y = y[indices]

    # 恢复维度顺序
    # y: [32, 64] ==> [64, 32]
    dim_ls = list(range(len(y.shape)))
    dim_ls = dim_ls[1:] + [0]
    y = y.transpose(*dim_ls)

    return y
