import pytest
import numpy as np
from kevin.patches.for_test import check_consistency
from kevin.computer_science.algorithm.search import binary_search


def test_binary_search():
    print("test search.binary_search()")

    # check _binary_search
    for _ in range(1000):
        # 随机构建输入
        ls = np.random.rand(100).tolist()
        value = ls.pop(-1)
        # 查找
        index_0 = binary_search(ls=ls, value=value, is_sorted=False)
        # 标准答案
        ls.append(value)
        ls.sort()
        index_1 = ls.index(value)
        # 检查
        check_consistency(index_0, index_1)
