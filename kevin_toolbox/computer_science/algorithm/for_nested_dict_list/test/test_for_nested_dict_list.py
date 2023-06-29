import copy
import pytest
import numpy as np
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.computer_science.algorithm import for_nested_dict_list as fndl


def test_get_value_by_name():
    print("test for_nested_dict_list.get_value_by_name()")

    x = dict(acc=[0.66, 0.78, 0.99], model_paras=dict(name="fuck", layers=(1, 2, 3)))

    # 多种名字
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

    # pop
    check_consistency(
        x["acc"][0], fndl.get_value_by_name(var=x, name=":acc@0", b_pop=True)
    )
    check_consistency(
        x["model_paras"]["layers"], fndl.get_value_by_name(var=x, name=":model_paras|layers", b_pop=True)
    )
    check_consistency(
        dict(acc=[0.78, 0.99], model_paras=dict(name="fuck")), x
    )

    # 取值失败时返回默认值
    try:
        fndl.get_value_by_name(var=x, name=":acc@2")
    except:
        assert True
    else:
        assert False
    check_consistency(
        None, fndl.get_value_by_name(var=x, name=":acc@2", default=None)
    )

    # 转义
    x = {
        'strategy': {
            ':settings:for_all:lr': [1, 2, 3]
        }
    }
    check_consistency(x["strategy"][":settings:for_all:lr"][1],
                      fndl.get_value_by_name(var=x, name=r":strategy:\:settings\:for_all\:lr@1"))


def test_set_value_by_name():
    print("test for_nested_dict_list.set_value_by_name()")

    x = dict(acc=[0.66, 0.78, 0.99])

    # 多种方式设置
    fndl.set_value_by_name(var=x, name="|acc|0", value=1)
    check_consistency(dict(acc=[1, 0.78, 0.99]), x)
    fndl.set_value_by_name(var=x, name="var:acc@0", value=2)
    check_consistency(dict(acc=[2, 0.78, 0.99]), x)

    # 强制设置（创建字典）
    fndl.set_value_by_name(var=x, name="www|acc|1|1", value=666, b_force=True)
    check_consistency(dict(acc=[2, {"1": 666}, 0.99]), x)
    check_consistency(fndl.get_value_by_name(var=x, name="www|acc|1|1"), 666)

    # 强制设置（创建列表）
    fndl.set_value_by_name(var=x, name="www|acc@4", value=0.1, b_force=True)
    check_consistency(dict(acc=[2, {"1": 666}, 0.99, None, 0.1]), x)

    # 特殊情况
    res = fndl.set_value_by_name(var=x, name="www", value=0.1, b_force=True)
    check_consistency(0.1, res)


def test_traverse():
    print("test for_nested_dict_list.traverse()")

    for traversal_mode in ["dfs_pre_order", "dfs_post_order", "bfs"]:
        x = [{"d": 3, "c@t": 4}, np.array([[1, 2, 3]])]

        # replace 模式
        x = fndl.traverse(var=x, match_cond=lambda _, k, v: type(v) is np.ndarray, action_mode="replace",
                          converter=lambda k, v: v.tolist(), traversal_mode=traversal_mode)
        check_consistency([{"d": 3, "c@t": 4}, [[1, 2, 3]]], x)

        # remove 模式
        x = fndl.traverse(var=x, match_cond=lambda _, k, v: v == 3, action_mode="remove", traversal_mode=traversal_mode)
        check_consistency([{"c@t": 4}, [[1, 2]]], x)

        # skip 模式（b_use_name_as_idx=True）
        leaf_nodes, values, names = [], [], []

        def func(_, idx, v):
            nonlocal leaf_nodes, values, names
            names.append(idx)
            if not isinstance(v, (list, dict,)):
                leaf_nodes.append(idx)
                values.append(v)
                return True
            else:
                return False

        fndl.traverse(var=x, match_cond=func, action_mode="skip", b_use_name_as_idx=True, traversal_mode=traversal_mode)
        check_consistency(sorted([r"@0:c\@t", "@1@0@0", "@1@0@1"]), sorted(leaf_nodes))
        for n, v in zip(leaf_nodes, values):
            check_consistency(v, fndl.get_value_by_name(var=x, name=n))

        # 遍历顺序
        if traversal_mode == "dfs_post_order":
            check_consistency(['@1@0@1', '@1@0@0', '@1@0', r'@0:c\@t', '@1', '@0'], names)
        elif traversal_mode == "dfs_pre_order":
            check_consistency(['@1', '@0', '@1@0', '@1@0@1', '@1@0@0', r'@0:c\@t'], names)
        else:
            check_consistency(['@1', '@0', '@1@0', r'@0:c\@t', '@1@0@1', '@1@0@0'], names)


def test_count_leaf_node_nums():
    print("test for_nested_dict_list.count_leaf_node_nums()")

    x = [dict(d=3, c=4), np.array([[1, 2, 3]])]
    check_consistency(3, fndl.count_leaf_node_nums(var=x))

    x = np.array([[1, 2, 3]])
    check_consistency(0, fndl.count_leaf_node_nums(var=x))


def test_get_nodes():
    print("test for_nested_dict_list.get_nodes()")

    x = [{"d": 3, "c@t": 4}, np.array([[1, 2, 3]])]
    for level in range(-5, 5):
        for b_strict in [True, False]:
            for name, value in fndl.get_nodes(var=x, level=level, b_strict=b_strict):
                check_consistency(value, fndl.get_value_by_name(var=x, name=name))
    #
    check_consistency(sorted([('@1', x[1]), ('@0:d', x[0]["d"]), (r'@0:c\@t', x[0]["c@t"])]),
                      sorted(fndl.get_nodes(var=x, level=-1, b_strict=True)),
                      sorted(fndl.get_nodes(var=x, level=-1, b_strict=False)))
    check_consistency(sorted([('', x), ('@0', x[0])]),
                      sorted(fndl.get_nodes(var=x, level=-2, b_strict=True)),
                      sorted(fndl.get_nodes(var=x, level=-2, b_strict=False)))
    check_consistency(sorted([('', x)]),
                      sorted(fndl.get_nodes(var=x, level=-3, b_strict=True)),
                      sorted(fndl.get_nodes(var=x, level=-3, b_strict=False)))
    check_consistency(sorted([]),
                      sorted(fndl.get_nodes(var=x, level=-4, b_strict=True)))
    check_consistency(sorted([('', x)]),
                      sorted(fndl.get_nodes(var=x, level=-4, b_strict=False)))
    #
    check_consistency(sorted([('', x)]),
                      sorted(fndl.get_nodes(var=x, level=0, b_strict=True)),
                      sorted(fndl.get_nodes(var=x, level=0, b_strict=False)))
    check_consistency(sorted([('@1', x[1]), ('@0', x[0])]),
                      sorted(fndl.get_nodes(var=x, level=1, b_strict=True)),
                      sorted(fndl.get_nodes(var=x, level=1, b_strict=False)))
    check_consistency(sorted([('@0:d', x[0]["d"]), (r'@0:c\@t', x[0]["c@t"])]),
                      sorted(fndl.get_nodes(var=x, level=2, b_strict=True)))
    for level in [2, 3, 4]:
        check_consistency(sorted([('@1', x[1]), ('@0:d', x[0]["d"]), (r'@0:c\@t', x[0]["c@t"])]),
                          sorted(fndl.get_nodes(var=x, level=level, b_strict=False)))
    for level in [3, 4]:
        check_consistency(sorted([]),
                          sorted(fndl.get_nodes(var=x, level=level, b_strict=True)))

    x = np.array([[1, 2, 3]])
    for level in range(-2, 2):
        for b_strict in [True, False]:
            for name, value in fndl.get_nodes(var=x, level=level, b_strict=b_strict):
                check_consistency(value, fndl.get_value_by_name(var=x, name=name))
    check_consistency([], fndl.get_nodes(var=x, level=-1))


def test_copy_():
    print("test for_nested_dict_list.copy_()")

    class A:
        version = 1.0

    for x in [
        None, "123", (1, 2, 3),
        dict(acc=[0.66, 0.78, 0.99], model_paras=dict(name="fuck", layers=({1, 2}, 2, 3)), scores=np.random.rand(100)),
        [dict(paras=[np.random.rand(100), np.random.rand(100), 0.99], ), 233],
        dict(a=dict(b=np.random.rand(100))),
        {'B': {'class': A}, 'var': {'c': 233}}
    ]:

        # 测试 深拷贝模式
        x_new = fndl.copy_(var=x, b_deepcopy=True)

        for name, v_old in fndl.get_nodes(var=x, level=-1):
            v_new = fndl.get_value_by_name(var=x_new, name=name)
            if id(copy.deepcopy(v_old)) != id(v_old):
                # 除了 int、str 等不可变对象之外，其他对象经过深拷贝之后应该指向另一个id
                assert id(v_new) != id(v_old), f'{name}'

        # 测试 浅拷贝模式
        x_new = fndl.copy_(var=x, b_deepcopy=False)
        # 叶节点指向同一个 id
        for name, v_old in fndl.get_nodes(var=x, level=-1):
            v_new = fndl.get_value_by_name(var=x_new, name=name)
            assert id(v_new) == id(v_old)
        # 父节点则指向不同 id
        level = -1
        while True:
            level -= 1
            nodes = fndl.get_nodes(var=x, level=level)
            if not nodes:
                break
            for name, v_old in nodes:
                v_new = fndl.get_value_by_name(var=x_new, name=name)
                assert id(v_new) != id(v_old), f'{name}'
