import math
import numpy as np
from kevin.machine_learning.patch_for_numpy.axis_and_dim import z_pattern


def generate_shuffle_index_ls(**kwargs):
    """
        生成随机的 index_ls 转置序列

        参数：
            shape:       维度
                            当维度大于1时，仅对最后一个维度进行单位化
                            例如，当 shape=(m,n,l) 时，保证有：
                                B[i,j,:] 是单位向量
            stride：
            kernel_size：卷积核的大小
            seed:       随机种子

        argmin_{n_i} stride[i] * n_i + kernel[i] >= shape[i]  s.t. n_i>=0

        n_i = math.ceil( max( shape[i]-kernel[i], 0 ) / stride[i] )
        对于由 (n_i,n_j,n_k) 指定的 crop
        它在原始feather map上的坐标为
        crop = x[ stride[i] * n_i: stride[i] * n_i + kernel[i], ... ]

        约定：
            - index_ls 将多维变量reshape(-1)后的坐标列表， shape [n_num, ]
            - indices_ls 多维变量的坐标列表， shape [n_num, index_num]

    """
    # 默认参数
    paras = {
        # 必要参数
        "shape": None,
        #
        "kernel_size": None,
        "stride": None,
        "seed": None,
        "allow_duplicates": False,
        #
        "generate_indices_func": z_pattern.generate_indices,
    }

    # 获取参数
    paras.update(kwargs)

    # 校验参数
    # shape
    if isinstance(paras["shape"], (int,)):
        paras["shape"] = [paras["shape"]]
    assert isinstance(paras["shape"], (tuple, list,)) and 0 < len(paras["shape"])
    shape = list(paras["shape"])
    # kernel_size
    if paras["kernel_size"] is None:
        paras["kernel_size"] = shape
    if isinstance(paras["kernel_size"], (int,)):
        paras["kernel_size"] = [paras["kernel_size"]] * len(shape)
    assert isinstance(paras["kernel_size"], (tuple, list,)) and 0 < len(paras["kernel_size"]) <= len(shape)
    kernel_size = list(paras["kernel_size"])
    # stride_ls
    if paras["stride"] is None:
        paras["stride"] = kernel_size
    if isinstance(paras["stride"], (int,)):
        paras["stride"] = [paras["stride"]] * len(kernel_size)
    assert isinstance(paras["stride"], (tuple, list,)) and len(paras["stride"]) == len(kernel_size)
    stride_ls = list(paras["stride"])
    # generate_indices_func
    assert callable(paras["generate_indices_func"])

    # 构建索引矩阵
    index_ls = np.arange(0, np.prod(shape))
    index_ls = index_ls.reshape(shape)
    if len(kernel_size) < len(shape):
        new_shape = [-1] + shape[-len(kernel_size):]
        index_ls = index_ls.reshape(new_shape)

    # 构建遍历顺序
    shape_of_blocks = []
    for w, k, s in zip(shape[-len(kernel_size):], kernel_size, stride_ls):
        shape_of_blocks.append(math.ceil(max(w - k, 0) / s) + 1)
    indices = paras["generate_indices_func"](shape=shape_of_blocks, convert_to_zip_type=False)
    beg_indices = indices * np.array([stride_ls])
    end_indices = beg_indices + np.array([kernel_size])

    # 随机生成器
    rd = np.random.RandomState(seed=paras["seed"])

    # 随机打乱
    for i in range(index_ls.shape[0]):
        for beg, end in zip(beg_indices, end_indices):
            x = index_ls[i]
            cmd = "x[" + ",".join([f"{int(b)}:{int(e)}" for b, e in zip(beg, end)]) + "]"
            crop = eval(cmd)
            crop[:] = rd.choice(crop.reshape(-1), crop.size, replace=paras["allow_duplicates"]).reshape(crop.shape)
    #
    index_ls = index_ls.reshape(-1)

    return index_ls


if __name__ == '__main__':
    shape = [3, 4, 4]
    index_ls = generate_shuffle_index_ls(shape=shape, stride_ls=[2, 2], kernel_size=[2, 2], seed=114)
    print(index_ls.reshape(shape))
