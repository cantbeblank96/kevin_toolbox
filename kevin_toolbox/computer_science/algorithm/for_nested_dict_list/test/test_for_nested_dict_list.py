import pytest
import numpy as np
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.computer_science.algorithm import for_nested_dict_list as fndl


def test_get_value_by_name():
    print("test for_nested_dict_list.get_value_by_name()")

    x = dict(acc=[0.66, 0.78, 0.99], model_paras=dict(name="fuck", layers=(1, 2, 3)))

    # 测试多种名字
    check_consistency(
        x["acc"][0], fndl.get_value_by_name(var=x, name="|acc|0"),
        fndl.get_value_by_name(var=x, name=":acc@0"), fndl.get_value_by_name(var=x, name="xxx:acc@0")
    )
    check_consistency(
        x["model_paras"]["name"], fndl.get_value_by_name(var=x, name="xxx|model_paras:name")
    )
    check_consistency(
        x["model_paras"]["layers"], fndl.get_value_by_name(var=x, name="x:model_paras:layers")
    )
    check_consistency(
        x, fndl.get_value_by_name(var=x, name="var")
    )


def test_set_value_by_name():
    print("test for_nested_dict_list.set_value_by_name()")

    x = dict(acc=[0.66, 0.78, 0.99])

    # 多种方式设置
    fndl.set_value_by_name(var=x, name="|acc|0", value=1)
    check_consistency(dict(acc=[1, 0.78, 0.99]), x)
    fndl.set_value_by_name(var=x, name="var:acc@0", value=2)
    check_consistency(dict(acc=[2, 0.78, 0.99]), x)

    # 强制设置
    fndl.set_value_by_name(var=x, name="www|acc|1|1", value=666, b_force=True)
    check_consistency(dict(acc=[2, {"1": 666}, 0.99]), x)
    check_consistency(fndl.get_value_by_name(var=x, name="www|acc|1|1"), 666)


def test_traverse():
    print("test for_nested_dict_list.traverse()")

    x = [dict(d=3, c=4), np.array([[1, 2, 3]])]

    # replace 模式
    x = fndl.traverse(var=x, match_cond=lambda _, k, v: type(v) is np.ndarray, action_mode="replace",
                      converter=lambda k, v: v.tolist())
    check_consistency([dict(d=3, c=4), [[1, 2, 3]]], x)

    # remove 模式
    x = fndl.traverse(var=x, match_cond=lambda _, k, v: v == 3, action_mode="remove")
    check_consistency([dict(c=4), [[1, 2]]], x)

    # skip 模式（b_use_name_as_idx=True）
    names, values = [], []

    def func(_, idx, v):
        nonlocal names, values
        if not isinstance(v, (list, dict,)):
            names.append(idx)
            values.append(v)
            return True
        else:
            return False

    fndl.traverse(var=x, match_cond=func, action_mode="skip", b_use_name_as_idx=True)
    check_consistency(sorted(["@0:c", "@1@0@0", "@1@0@1"]), sorted(names))

    for n, v in zip(names, values):
        check_consistency(v, fndl.get_value_by_name(var=x, name=n))


def test_count_leaf_node_nums():
    print("test for_nested_dict_list.count_leaf_node_nums()")

    x = [dict(d=3, c=4), np.array([[1, 2, 3]])]
    check_consistency(3, fndl.count_leaf_node_nums(var=x))

    x = np.array([[1, 2, 3]])
    check_consistency(0, fndl.count_leaf_node_nums(var=x))


def test_get_leaf_nodes():
    print("test for_nested_dict_list.get_leaf_nodes()")

    x = [dict(d=3, c=4), np.array([[1, 2, 3]])]
    for name, value in fndl.get_leaf_nodes(var=x):
        check_consistency(value, fndl.get_value_by_name(var=x, name=name))

    x = np.array([[1, 2, 3]])
    check_consistency([], fndl.get_value_by_name(var=x))
