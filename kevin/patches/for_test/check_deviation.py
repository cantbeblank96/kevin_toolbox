import numpy as np
import torch


def check_deviation(*args, epsilon=1e-7, verbose=False):
    """
        检查 args 中多个数据之间的差值，当差值超过给定的 epsilon 时则报错
            支持 np.array 和 torch.tensor 以及两种类型的混合
    """
    assert len(args) >= 2
    assert isinstance(epsilon, (int, float,))

    args = [v.cpu().numpy() if torch.is_tensor(v) else v for v in args]

    for v in args[1:]:
        deviation = np.max(np.abs(args[0] - v))
        if verbose:
            print(f"deviation : {deviation}")
        assert deviation < epsilon
