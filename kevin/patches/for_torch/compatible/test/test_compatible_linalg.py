import pytest
import importlib
import sys
import random
import numpy as np
import torch
from kevin.patches.for_test import check_consistency
from kevin.patches.for_torch.compatible import linalg

"""
建议在最新版本的 pytorch 以及 gpu 可用的环境下运行本测试脚本
    本模块 for_torch.compatible 对低版本的兼容，本质上是用低版本中的函数去实现高版本的功能
    因此只有在高版本的 pytorch 下才能同时运行低版本的实现，并与高版本的运行结果进行比对
"""


def test_norm():
    print("test compatible.linalg.norm()")

    ver_bak = torch.__version__

    for _ in range(100):
        # 随机构建输入的
        shape = [np.random.randint(1, 10) for _ in range(np.random.randint(1, 4))]
        x = torch.rand(shape)
        if np.random.randint(2) % 2 == 1 and len(shape) > 1:
            # If :attr:`dim` is a `2`-`tuple`, the matrix norm will be computed.
            dim = sorted(np.random.choice(range(len(shape)), size=2, replace=False).tolist())
            ord = random.choice(["fro", 1, 2])
        else:
            # If :attr:`dim` is an `int`, the vector norm will be computed
            dim = np.random.randint(len(shape))
            ord = random.choice([1, 2, torch.inf])
        if torch.cuda.is_available() and np.random.randint(2) % 2 == 1:
            x = x.to(device=torch.device("cuda"))
        keepdim = np.random.randint(2) % 2 == 1

        #
        res = []
        for ver in ["1.0", "1.12"]:
            torch.__version__ = ver
            importlib.reload(sys.modules["kevin.patches.for_torch.compatible.linalg.norm"])
            res.append(linalg.norm(x, ord=ord, dim=dim, keepdim=keepdim))

        # 检验
        check_consistency(*res, tolerance=1e-10)

    torch.__version__ = ver_bak


def test_tile():
    print("test compatible.linalg.svd()")

    ver_bak = torch.__version__

    for _ in range(100):
        # 随机构建输入的
        shape = [np.random.randint(1, 10) for _ in range(np.random.randint(2, 4))]
        x = torch.rand(shape)
        if torch.cuda.is_available() and np.random.randint(2) % 2 == 1:
            x = x.to(device=torch.device("cuda"))
        full_matrices = np.random.randint(2) % 2 == 1

        #
        res = []
        for ver in ["1.0", "1.12"]:
            torch.__version__ = ver
            importlib.reload(sys.modules["kevin.patches.for_torch.compatible.linalg.svd"])
            res.append(linalg.svd(x, full_matrices=full_matrices))

        # 检验
        for temp in zip(*res):
            check_consistency(*temp, tolerance=1e-10)

    torch.__version__ = ver_bak
