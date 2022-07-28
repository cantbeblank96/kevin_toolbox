import math

import numpy as np


def padding(**kwargs):
    """
    在自由模式下，padding_kwargs中需要设定margin_ls参数，而且该参数应该是与x.shape同样长度的列表。 支持非对称 padding
    卷积的三种模式full, same, valid： https://zhuanlan.zhihu.com/p/62760780
    """
    """
        对 shape 内的各个 block 中的坐标进行打乱，生成随机打乱的 index_ls
            index_ls 的具体定义参见 coordinates.convert()
            参照卷积的形式，按照 kernel_size 和 stride 对 shape 的最后几个维度进行遍历，依次对遍历经过的 block 进行内部随机打乱。
            支持通过指定 generate_indices_ls_func 来设置对 block 的遍历顺序/模式。

        参数：
            x:                      
            padding_mode：                扩展边缘的方式
                                            支持以下四种方式：
                                                full, same, valid, free
                                                其中 full, same, valid 的介绍参见： https://zhuanlan.zhihu.com/p/62760780
                                                在 free 模式下，你将可以自由地 设置每一个维度的两个边缘的扩展大小
                                            默认使用 same 模式
            padding_kwargs：                     卷积的步长
                                            默认为 None 表示与 kernel_size 相等
            filling_mode:                       随机种子
            filling_kwargs:           允许出现重复值。
                                            默认为 False
            generate_func_of_traversal_order_for_blocks：  用于指定对 block 的遍历顺序
                                            默认使用 coordinates.generate(pattern="z_pattern", output_format="indices_ls") 进行遍历
                                            你也可以自定义一个根据参数 shape 生成 zip_indices 格式的坐标列表的函数，来指定遍历顺序

        blocks 相关变量的计算公式：
            第i个维度上 block 的数量 n_i = argmin_{n_i} stride[i] * n_i + kernel[i] >= shape[i]  s.t. n_i>=0
                            等效于： n_i = math.ceil( max( shape[i]-kernel[i], 0 ) / stride[i] )
            对于由 (n_i,n_j,n_k) 指定的 crop，它在原始feather map上的坐标为：
                                crop = x[ stride[i] * n_i: stride[i] * n_i + kernel[i], ... ]
    """
    # 默认参数
    paras = {
        # 必要参数
        "x": None,
        #
        "padding_mode": "same",
        "padding_kwargs": dict(),
        "filling_mode": "copy_edge",
        "filling_kwargs": dict(),
    }

    # 获取参数
    paras.update(kwargs)

    # 校验参数
    assert paras["padding_mode"] in ["full", "same", "valid", "free"]
    padding_mode = paras["padding_mode"]
    assert paras["filling_mode"] in ["copy_edge", "value"]
    filling_mode = paras["filling_mode"]
    assert [isinstance(paras[key], (dict,)) for key in {"padding_kwargs", "filling_kwargs"}]
    padding_kwargs, filling_kwargs = paras["padding_kwargs"], paras["filling_kwargs"]
    assert paras["x"] is not None
    x = paras["x"]

    # 获取 margin_ls
    margin_ls = None
    if padding_mode == "free":
        assert "margin_ls" in padding_kwargs and isinstance(padding_kwargs["margin_ls"], (list, tuple,)) \
               and len(padding_kwargs["margin_ls"]) == len(x.shape), \
            f"In {padding_mode} mode, padding_kwargs should has margin_ls parameter, " \
            f"and margin_ls should be a list of the same length as x.shape."
        margin_ls = list(padding_kwargs["margin_ls"])
        for i, margins in enumerate(margin_ls):
            if isinstance(margins, (int,)):
                margins = [margins, margins]
            assert isinstance(margins, (list, tuple,)) and len(margins) == 2 and \
                   [m for m in margins if isinstance(m, (int,)) and m >= 0]
            margin_ls[i] = margins
    elif padding_mode in ["full", "same", "valid"]:
        assert "kernel_size" in padding_kwargs and isinstance(padding_kwargs["kernel_size"], (int, list, tuple,)), \
            f"In {padding_mode} mode, padding_kwargs should has kernel_size parameter, " \
            f"and kernel_size should be an integer or list of the same length as x.shape."
        kernel_size = padding_kwargs["kernel_size"]
        if isinstance(kernel_size, (int,)):
            kernel_size = [kernel_size] * len(x.shape)
        assert len(kernel_size) == len(x.shape)
        #
        if padding_mode == "full":
            margin_ls = [[math.ceil(i / 2)] * 2 for i in kernel_size]
        elif padding_mode == "same":
            margin_ls = [[math.floor(i / 2)] * 2 for i in kernel_size]
        else:
            margin_ls = [[0] * 2 for _ in kernel_size]
    assert margin_ls is not None

    # 构建基底+预填充
    new_shape = [m0 + dims + m1 for (m0, m1), dims in zip(margin_ls, x.shape)]
    y = None
    if filling_mode == "value":
        assert "default_value" in filling_kwargs and isinstance(filling_kwargs["default_value"], (int, float,))
        default_value = filling_kwargs["default_value"]
        if default_value == 0:
            y = np.zeros(shape=new_shape)
        else:
            y = np.ones(shape=new_shape) * default_value
    else:
        y = np.zeros(shape=new_shape)
    assert y is not None

    # 放置 crop
    exec(f"y[{','.join([f'{m0}:{-m1}' for m0, m1 in margin_ls])}]=x")

    # 后填充
    if filling_mode == "copy_edge":
        for i, (m0, m1) in enumerate(margin_ls):
            cmd = [':'] * len(margin_ls)
            # 上边缘
            if m0 > 0:
                cmd[i] = f":{m0}"
                cmd_0 = ','.join(cmd)
                cmd[i] = f"{m0}:{m0 + 1}"
                cmd_1 = ','.join(cmd)
                print(f"y[{cmd_0}]=y[{cmd_1}]")
                exec(f"y[{cmd_0}]=y[{cmd_1}]")
            # 下边缘
            if m1 > 0:
                cmd[i] = f"{-m1}:"
                cmd_0 = ','.join(cmd)
                cmd[i] = f"{-m1 - 1}:{-m1}"
                cmd_1 = ','.join(cmd)
                print(f"y[{cmd_0}]=y[{cmd_1}]")
                exec(f"y[{cmd_0}]=y[{cmd_1}]")

    return y


if __name__ == '__main__':
    shape_ = [3, 2, 2]
    y_ = padding(x=np.random.normal(size=shape_), padding_mode="same", padding_kwargs=dict(kernel_size=3),
                 filling_mode="copy_edge",
                 filling_kwargs=dict(default_value=3))
    print(y_)
    print(y_.shape)
