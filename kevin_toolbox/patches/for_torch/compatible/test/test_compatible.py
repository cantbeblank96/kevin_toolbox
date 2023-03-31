import pytest
import importlib
import sys
import numpy as np
import torch
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.patches.for_torch import compatible
from kevin_toolbox.env_info import version

"""
建议在最新版本的 pytorch 以及 gpu 可用的环境下运行本测试脚本
    本模块 for_torch.compatible 对低版本的兼容，本质上是用低版本中的函数去实现高版本的功能
    因此只有在高版本的 pytorch 下才能同时运行低版本的实现，并与高版本的运行结果进行比对
"""


def test_concat():
    print("test compatible.concat()")

    ver_bak = torch.__version__

    for _ in range(100):
        # 随机构建输入的
        shape_0 = [np.random.randint(1, 10) for _ in range(np.random.randint(1, 4))]
        shape_1 = shape_0[:]
        dim = np.random.randint(len(shape_1))
        shape_1[dim] = np.random.randint(1, 10)
        x_0, x_1 = torch.rand(shape_0), torch.rand(shape_1)
        if torch.cuda.is_available() and np.random.randint(2) % 2 == 1:
            x_0 = x_0.to(device=torch.device("cuda"))
            x_1 = x_1.to(device=torch.device("cuda"))

        #
        res = []
        for ver in ["1.0", "1.12"]:
            ver = ver_bak if version.compare(ver, ">", ver_bak) else ver
            torch.__version__ = ver
            importlib.reload(sys.modules["kevin_toolbox.patches.for_torch.compatible.concat"])
            res.append(compatible.concat((x_0, x_1), dim=dim))

        # 检验
        check_consistency(*res)

    torch.__version__ = ver_bak


def test_tile():
    print("test compatible.tile()")

    ver_bak = torch.__version__

    for _ in range(100):
        # 随机构建输入的
        shape = [np.random.randint(1, 10) for _ in range(np.random.randint(1, 4))]
        x = torch.rand(shape)
        multiples = [np.random.randint(1, 10) for _ in range(np.random.randint(len(shape)))]

        if torch.cuda.is_available() and np.random.randint(2) % 2 == 1:
            x = x.to(device=torch.device("cuda"))

        #
        res = []
        for ver in ["1.0", "1.12"]:
            ver = ver_bak if version.compare(ver, ">", ver_bak) else ver
            torch.__version__ = ver
            importlib.reload(sys.modules["kevin_toolbox.patches.for_torch.compatible.tile"])
            res.append(compatible.tile(x, multiples=multiples))

        # 检验
        check_consistency(*res)

    torch.__version__ = ver_bak


def test_where():
    print("test compatible.where()")

    ver_bak = torch.__version__

    for _ in range(100):
        # 随机构建输入的
        shape = [np.random.randint(1, 10) for _ in range(np.random.randint(1, 4))]
        if np.random.randint(2) % 2 == 1:
            # 测试 torch.where(condition, x, y) 的用法
            x = torch.rand(shape)
            y = torch.rand(shape)
            args = [x > 0, x, y]
        else:
            # 测试 torch.where(condition) 的用法
            x = torch.rand(shape)
            args = [x > 0]

        if torch.cuda.is_available() and np.random.randint(2) % 2 == 1:
            args = [i.to(device=torch.device("cuda")) for i in args]

        #
        res = []
        for ver in ["1.0", "1.12"]:
            ver = ver_bak if version.compare(ver, ">", ver_bak) else ver
            torch.__version__ = ver
            importlib.reload(sys.modules["kevin_toolbox.patches.for_torch.compatible.where"])
            res.append(compatible.where(*args))

        # 检验
        for temp in zip(*res):
            check_consistency(*temp)

    torch.__version__ = ver_bak
