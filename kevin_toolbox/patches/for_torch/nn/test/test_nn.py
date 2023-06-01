import pytest
import torch
import torch.nn.functional as F
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.patches.for_torch import nn


def test_Lambda_Layer():
    print("test nn.Lambda_Layer")

    x = torch.randn([10, 3, 3])
    layer = nn.Lambda_Layer(func=F.relu)

    # 检验
    check_consistency(layer(x), F.relu(x))
