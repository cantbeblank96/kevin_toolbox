import numpy as np


def generate_kernel_for_mean_blur(**kwargs):
    """
        生成 均值模糊 的卷积核

        参数：
            shape:                      形状

        计算公式：
            kernel = E / n ，其中 E 表示全一矩阵，n为矩阵中元素的数量
    """
    # 默认参数
    paras = {
        # 必要参数
        "shape": None,
    }

    # 获取参数
    paras.update(kwargs)

    # 校验参数
    # shape
    assert isinstance(paras["shape"], (tuple, list,)) and 0 < len(paras["shape"])
    shape = list(paras["shape"])

    kernel = np.ones(shape=shape, dtype=np.float32) / np.prod(shape)
    return kernel


if __name__ == '__main__':
    kernel = generate_kernel_for_mean_blur(shape=[2, 3, 4])
    print(kernel)
    print(np.sum(kernel))
