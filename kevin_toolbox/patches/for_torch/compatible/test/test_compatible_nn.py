import pytest
import importlib
import sys
import random
import numpy as np
import torch
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.patches.for_torch.compatible import nn
from kevin_toolbox.env_info import version

"""
建议在最新版本的 pytorch 以及 gpu 可用的环境下运行本测试脚本
    本模块 for_torch.compatible 对低版本的兼容，本质上是用低版本中的函数去实现高版本的功能
    因此只有在高版本的 pytorch 下才能同时运行低版本的实现，并与高版本的运行结果进行比对
"""


def test_Sequential():
    print("test compatible.nn.Sequential")

    ver_bak = torch.__version__

    #
    res = []
    for ver in ["1.0", "1.12"]:
        ver = ver_bak if version.compare(ver, ">", ver_bak, mode="short") else ver
        torch.__version__ = ver
        importlib.reload(sys.modules["kevin_toolbox.patches.for_torch.compatible.nn.sequential"])

        stem = nn.Sequential()
        stem.add_module('conv', torch.nn.Conv2d(3, 3, 10))
        res.append(f'{stem.get_submodule("conv")}')
    # 检验
    check_consistency(*res)

    torch.__version__ = ver_bak
