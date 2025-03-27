import copy
import pytest
import numpy as np
from kevin_toolbox.patches.for_test import check_consistency
import kevin_toolbox.nested_dict_list as ndl


def test_traverse_for_skip_repeated_0():
    """
        增加 b_skip_repeated_non_leaf_node 参数，用于避免对重复非叶节点进行多次反复处理
            该功能默认为根据 action_mode 的情况决定关闭或开启
    """

    # data
    transforms_s = [
        "123"
    ]

    content = {
        "for_val": transforms_s,
        "for_test": transforms_s
    }

    # 不使用 b_skip_repeated_non_leaf_node=False 时，将会导致对 transforms_s 中的 "123" 进行两次处理。
    res = ndl.traverse(var=copy.deepcopy(content),
                       match_cond=lambda _, __, v: isinstance(v, str), action_mode="replace",
                       converter=lambda _, x: "<eval>" + x,
                       b_traverse_matched_element=True,
                       b_skip_repeated_non_leaf_node=False)

    for n, v in ndl.get_nodes(var=res, level=-1, b_strict=True):
        with pytest.raises(AssertionError):
            check_consistency(v, "<eval>123")
        check_consistency(v, "<eval><eval>123")

    # 使用 b_skip_repeated_non_leaf_node=True 时，将会导致对 "123" 进行一次处理，符合期望。
    res = ndl.traverse(var=copy.deepcopy(content),
                       match_cond=lambda _, __, v: isinstance(v, str), action_mode="replace",
                       converter=lambda _, x: "<eval>" + x,
                       b_traverse_matched_element=True,
                       b_skip_repeated_non_leaf_node=True)

    for n, v in ndl.get_nodes(var=res, level=-1, b_strict=True):
        check_consistency(v, "<eval>123")


def test_traverse_for_skip_repeated_1():
    """
        增加 cond_for_repeated_leaf_to_skip 参数，用于在特殊情况下，支持不对重复叶节点进行多次反复处理
            该功能默认不开启
    """
    # data
    count = np.zeros(1)

    def add_one():
        nonlocal count
        count += 1

    content = {
        "for_val": add_one,
        "for_test": add_one
    }

    #
    res = ndl.traverse(var=copy.deepcopy(content),
                       match_cond=lambda _, __, v: callable(v), action_mode="replace",
                       converter=lambda _, x: x(),
                       b_traverse_matched_element=True,
                       cond_for_repeated_leaf_to_skip=None)
    check_consistency(count[0], 2)

    #
    count[:] = 0
    res = ndl.traverse(var=copy.deepcopy(content),
                       match_cond=lambda _, __, v: callable(v), action_mode="replace",
                       converter=lambda _, x: x(),
                       b_traverse_matched_element=True,
                       cond_for_repeated_leaf_to_skip=[lambda x: callable(x)])
    check_consistency(count[0], 1)
