import copy
from collections import defaultdict
import pytest
import torch
import numpy as np
from kevin_toolbox.patches.for_test import check_consistency
import kevin_toolbox.nested_dict_list as ndl


def test_get_value():
    print("test nested_dict_list.get_value()")

    x = dict(acc=[0.66, 0.78, 0.99], model_paras=dict(name="fuck", layers=(1, 2, 3)))

    # 多种名字
    check_consistency(
        x["acc"][0], ndl.get_value(var=x, name="|acc|0"),
        ndl.get_value(var=x, name=":acc@0"), ndl.get_value(var=x, name="xxx:acc@0")
    )
    check_consistency(
        x["model_paras"]["name"], ndl.get_value(var=x, name="xxx|model_paras:name")
    )
    check_consistency(
        x["model_paras"]["layers"], ndl.get_value(var=x, name="x:model_paras:layers")
    )
    check_consistency(
        x, ndl.get_value(var=x, name="var")
    )

    # pop
    check_consistency(
        x["acc"][0], ndl.get_value(var=x, name=":acc@0", b_pop=True)
    )
    check_consistency(
        x["model_paras"]["layers"], ndl.get_value(var=x, name=":model_paras|layers", b_pop=True)
    )
    check_consistency(
        dict(acc=[0.78, 0.99], model_paras=dict(name="fuck")), x
    )

    # 取值失败时返回默认值
    with pytest.raises(IndexError):
        ndl.get_value(var=x, name=":acc@2")
    check_consistency(
        None, ndl.get_value(var=x, name=":acc@2", default=None)
    )

    # 转义
    x = {
        'strategy': {
            ':settings:for_all:lr': [1, 2, 3]
        }
    }
    check_consistency(x["strategy"][":settings:for_all:lr"][1],
                      ndl.get_value(var=x, name=r":strategy:\:settings\:for_all\:lr@1"))


def test_set_value_0():
    print("test nested_dict_list.set_value()")

    x = dict(acc=[0.66, 0.78, 0.99])

    # 多种方式设置
    ndl.set_value(var=x, name="|acc|0", value=1)
    check_consistency(dict(acc=[1, 0.78, 0.99]), x)
    ndl.set_value(var=x, name="var:acc@0", value=2)
    check_consistency(dict(acc=[2, 0.78, 0.99]), x)

    # 强制设置（创建字典）
    ndl.set_value(var=x, name="www|acc|1|1", value=666, b_force=True)
    check_consistency(dict(acc=[2, {"1": 666}, 0.99]), x)
    check_consistency(ndl.get_value(var=x, name="www|acc|1|1"), 666)

    # 强制设置（创建列表）
    ndl.set_value(var=x, name="www|acc@4", value=0.1, b_force=True)
    check_consistency(dict(acc=[2, {"1": 666}, 0.99, None, 0.1]), x)

    # 特殊情况
    res = ndl.set_value(var=x, name="www", value=0.1, b_force=True)
    check_consistency(0.1, res)


def test_set_value_1():
    print("test nested_dict_list.set_value()")

    # 为了验证bug（无法强制设置以@开头的name）是否修复
    y = ndl.set_value(var=None, name="@1", value=1, b_force=True)
    check_consistency([None, 1], y)


def test_set_value_2():
    """
        为了验证以下bug是否修复：
            - 无法在 var=None 对 var 进行多层强制的设置
    """
    print("test nested_dict_list.set_value()")

    #
    y = ndl.set_value(var=None, name=":1", value=1, b_force=True)
    check_consistency({"1": 1}, y)

    #
    y = ndl.set_value(var=None, name=":1:2", value=1, b_force=True)
    check_consistency({"1": {"2": 1}}, y)
    #
    y = ndl.set_value(var=None, name=":1@2", value=1, b_force=True)
    check_consistency({"1": [None, None, 1]}, y)


def test_set_value_3():
    """
        为了验证以下bug是否修复：
            - 对于method=@,但是node不为正整数的name，错误地使用了list进行构建
    """
    print("test nested_dict_list.set_value()")

    #
    name = ":for_exp:optimizer:ema_s:for_first_moment@(0, 55)"
    value = 233

    var = ndl.set_value(var=None, name=name, value=value, b_force=True)

    #
    check_consistency(ndl.get_value(var=var, name=name), value)
    check_consistency(var, {'for_exp': {'optimizer': {'ema_s': {'for_first_moment': {(0, 55): value}}}}})


def test_set_default():
    print("test nested_dict_list.set_default()")

    x = None

    # 不存在时创建
    x = ndl.set_default(var=x, name=":model_paras:name", default="fuck", b_force=True)
    check_consistency(dict(model_paras=dict(name="fuck", )), x)

    # 存在时不创建
    #   当给定有 cache 时，只要经过检查就添加到 cache 中
    cache = set()
    x = ndl.set_default(var=x, name=":model_paras:name", default="you", b_force=True, cache_for_verified_names=cache)
    check_consistency(dict(model_paras=dict(name="fuck", )), x)
    check_consistency({":model_paras:name", }, cache)

    # 当给定有 cache 时，只要检测到 name 在 cache 中，就直接跳过 set_default
    cache.add(":model_paras:layers")
    x = ndl.set_default(var=x, name=":model_paras:layers", default=(1, 2, 3), b_force=True,
                        cache_for_verified_names=cache)
    check_consistency(dict(model_paras=dict(name="fuck", )), x)


def test_traverse_0():
    print("test nested_dict_list.traverse()")

    for traversal_mode in ["dfs_pre_order", "dfs_post_order", "bfs"]:
        x = [{"d": 3, "c@t": 4}, np.array([[1, 2, 3]])]

        # replace 模式
        x = ndl.traverse(var=x, match_cond=lambda _, k, v: type(v) is np.ndarray, action_mode="replace",
                         converter=lambda k, v: v.tolist(), traversal_mode=traversal_mode)
        check_consistency([{"d": 3, "c@t": 4}, [[1, 2, 3]]], x)

        # remove 模式
        x = ndl.traverse(var=x, match_cond=lambda _, k, v: v == 3, action_mode="remove", traversal_mode=traversal_mode)
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

        ndl.traverse(var=x, match_cond=func, action_mode="skip", b_use_name_as_idx=True, traversal_mode=traversal_mode)
        check_consistency(sorted([r"@0:c\@t", "@1@0@0", "@1@0@1"]), sorted(leaf_nodes))
        for n, v in zip(leaf_nodes, values):
            check_consistency(v, ndl.get_value(var=x, name=n))

        # 遍历顺序
        if traversal_mode == "dfs_post_order":
            check_consistency(['@1@0@1', '@1@0@0', '@1@0', r'@0:c\@t', '@1', '@0'], names)
        elif traversal_mode == "dfs_pre_order":
            check_consistency(['@1', '@0', '@1@0', '@1@0@1', '@1@0@0', r'@0:c\@t'], names)
        else:
            check_consistency(['@1', '@0', '@1@0', r'@0:c\@t', '@1@0@1', '@1@0@0'], names)


def test_traverse_1():
    print("test nested_dict_list.traverse()")

    x = [{"d": 3, "c@t": 4, 5: 6}, 2, (1, 2, 3)]

    # 验证名字的正确性
    idx_ls, value_ls = [], []

    def converter(idx, value):
        idx_ls.append(idx)
        value_ls.append(value)
        return value

    x = ndl.traverse(var=x, match_cond=lambda _, __, ___: True, action_mode="replace", converter=converter,
                     b_use_name_as_idx=True, b_traverse_matched_element=True)
    for idx, value in zip(idx_ls, value_ls):
        check_consistency(id(value), id(ndl.get_value(var=x, name=idx)))


def test_count_leaf_node_nums():
    print("test nested_dict_list.count_leaf_node_nums()")

    x = [dict(d=3, c=4), np.array([[1, 2, 3]])]
    check_consistency(3, ndl.count_leaf_node_nums(var=x))

    x = np.array([[1, 2, 3]])
    check_consistency(0, ndl.count_leaf_node_nums(var=x))


def test_get_nodes():
    print("test nested_dict_list.get_nodes()")

    x = [{"d": 3, "c@t": 4}, np.array([[1, 2, 3]])]
    for level in range(-5, 5):
        for b_strict in [True, False]:
            for name, value in ndl.get_nodes(var=x, level=level, b_strict=b_strict):
                check_consistency(value, ndl.get_value(var=x, name=name))
    #
    check_consistency(sorted([('@1', x[1]), ('@0:d', x[0]["d"]), (r'@0:c\@t', x[0]["c@t"])]),
                      sorted(ndl.get_nodes(var=x, level=-1, b_strict=True)),
                      sorted(ndl.get_nodes(var=x, level=-1, b_strict=False)))
    check_consistency(sorted([('', x), ('@0', x[0])]),
                      sorted(ndl.get_nodes(var=x, level=-2, b_strict=True)),
                      sorted(ndl.get_nodes(var=x, level=-2, b_strict=False)))
    check_consistency(sorted([('', x)]),
                      sorted(ndl.get_nodes(var=x, level=-3, b_strict=True)),
                      sorted(ndl.get_nodes(var=x, level=-3, b_strict=False)))
    check_consistency(sorted([]),
                      sorted(ndl.get_nodes(var=x, level=-4, b_strict=True)))
    check_consistency(sorted([('', x)]),
                      sorted(ndl.get_nodes(var=x, level=-4, b_strict=False)))
    #
    check_consistency(sorted([('', x)]),
                      sorted(ndl.get_nodes(var=x, level=0, b_strict=True)),
                      sorted(ndl.get_nodes(var=x, level=0, b_strict=False)))
    check_consistency(sorted([('@1', x[1]), ('@0', x[0])]),
                      sorted(ndl.get_nodes(var=x, level=1, b_strict=True)),
                      sorted(ndl.get_nodes(var=x, level=1, b_strict=False)))
    check_consistency(sorted([('@0:d', x[0]["d"]), (r'@0:c\@t', x[0]["c@t"])]),
                      sorted(ndl.get_nodes(var=x, level=2, b_strict=True)))
    for level in [2, 3, 4]:
        check_consistency(sorted([('@1', x[1]), ('@0:d', x[0]["d"]), (r'@0:c\@t', x[0]["c@t"])]),
                          sorted(ndl.get_nodes(var=x, level=level, b_strict=False)))
    for level in [3, 4]:
        check_consistency(sorted([]),
                          sorted(ndl.get_nodes(var=x, level=level, b_strict=True)))

    x = np.array([[1, 2, 3]])
    for level in range(-2, 2):
        for b_strict in [True, False]:
            for name, value in ndl.get_nodes(var=x, level=level, b_strict=b_strict):
                check_consistency(value, ndl.get_value(var=x, name=name))
    check_consistency([], ndl.get_nodes(var=x, level=-1))


def test_copy_0():
    print("test nested_dict_list.copy_()")

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
        x_new = ndl.copy_(var=x, b_deepcopy=True)

        for name, v_old in ndl.get_nodes(var=x, level=-1):
            v_new = ndl.get_value(var=x_new, name=name)
            if id(copy.deepcopy(v_old)) != id(v_old):
                # 除了 int、str 等不可变对象之外，其他对象经过深拷贝之后应该指向另一个id
                assert id(v_new) != id(v_old), f'{name}'

        # 测试 浅拷贝模式
        x_new = ndl.copy_(var=x, b_deepcopy=False)
        # 叶节点指向同一个 id
        for name, v_old in ndl.get_nodes(var=x, level=-1):
            v_new = ndl.get_value(var=x_new, name=name)
            assert id(v_new) == id(v_old)
        # 父节点则指向不同 id
        for name, v_old in _get_non_leaf_nodes(var=x):
            v_new = ndl.get_value(var=x_new, name=name)
            assert id(v_new) != id(v_old), f'{name}'


def test_copy_1():
    print("test nested_dict_list.copy_()")

    """
    本测试用例主要测试是否修复无法复制带有 grad_func 的tensor的问题
    
    起因：
        直接使用 copy.deepcopy 去复制带有非空 grad_func 的tensor将会报错：
            RuntimeError: Only Tensors created explicitly by the user (graph leaves) support the deepcopy protocol at the moment
    解决方法：
        参考 https://discuss.pytorch.org/t/copy-deepcopy-vs-clone/55022/10，使用 x.detach().clone() 来复制 tensor
        
    实例：
        t = torch.tensor([1,2,3.5],dtype=torch.float32, requires_grad=True, device='cuda:0')
        copy.deepcopy(t)
        # 不会报错
        t1 = t[:2]  # tensor([1., 2.], device='cuda:0', grad_fn=<SliceBackward0>)
        copy.deepcopy(t1)
        # 报错
        t1.detach().clone() # tensor([1., 2.], device='cuda:0')
        # 不报错
        
    局限：
        对于其他不支持deepcopy或者内部含有不支持deepcopy的变量，仍然是无法复制的，比如使用上面实例中的 t1 构建这样一个 tuple：
            (t1, t1, )
        则 ndl.copy_ 仍然无法对齐实现深复制
    """

    t = torch.tensor([1, 2, 3.5], dtype=torch.float32, requires_grad=True, device='cuda:0')
    t1 = t[:2]
    t2 = t1[:1]

    for x in [
        t, t1, t2,
        dict(t=t, t1=t1, t2=t2),
        [t, t1, t2],
        # (t, t1, t2)
    ]:
        # 测试 深拷贝模式
        x_new = ndl.copy_(var=x, b_deepcopy=True)

        for name, v_old in ndl.get_nodes(var=x, level=-1):
            v_new = ndl.get_value(var=x_new, name=name)
            # 除了 int、str 等不可变对象之外，其他对象经过深拷贝之后应该指向另一个id
            assert id(v_new) != id(v_old), f'{name}'

        # 测试 浅拷贝模式
        x_new = ndl.copy_(var=x, b_deepcopy=False)
        # 叶节点指向同一个 id
        for name, v_old in ndl.get_nodes(var=x, level=-1):
            v_new = ndl.get_value(var=x_new, name=name)
            assert id(v_new) == id(v_old)
        # 父节点则指向不同 id
        for name, v_old in _get_non_leaf_nodes(var=x):
            v_new = ndl.get_value(var=x_new, name=name)
            assert id(v_new) != id(v_old), f'{name}'


def _get_non_leaf_nodes(var):
    level = -1
    res = []
    while True:
        level -= 1
        nodes = ndl.get_nodes(var=var, level=level, b_strict=True)
        if not nodes:
            break
        res.extend(nodes)
    return res


def test_copy_2():
    print("test nested_dict_list.copy_()")

    """
    测试 copy_ 中的 b_keep_internal_references 参数
        该参数用于决定是否保留内部的引用关系
    """

    # 测试数据
    """
    以下面的结构为例（<xx>表示该结构体/节点内存中的地址）：
        {<0>
            "a": [<1>
                {<2> 1, 2, 3},
                {<3> 4, 5, 6),
                {<2> 1, 2, 3}
            ],
            "b": [<1>
                {<2> 1, 2, 3},
                {<3> 4, 5, 6),
                {<2> 1, 2, 3}
            ],
        }
    """
    set_0, set_1 = {1, 2, 3}, {4, 5, 6}
    ls = [set_0, set_1, set_0]
    x = dict(a=ls, b=ls)

    def _judge_node_ids_consistent(var_0, var_1, part="leaf"):
        """
            计算输入的 var_0 和 var_1 中节点的id的差异

            返回：
                {
                    "same": [<node_name>, ...],  # node name with same id in both var_0 and var_1
                    "diff":[<node_name>, ...]
                }
        """
        nodes_0 = ndl.get_nodes(var=var_0, level=-1) if part == "leaf" else _get_non_leaf_nodes(var=var_0)
        nodes_1 = ndl.get_nodes(var=var_1, level=-1) if part == "leaf" else _get_non_leaf_nodes(var=var_1)
        res_0 = {name: id(v) for name, v in nodes_0}
        res_1 = {name: id(v) for name, v in nodes_1}
        check_consistency(sorted(list(res_0.keys())), sorted(list(res_1.keys())))
        same, diff = set(), set()
        for k in res_0:
            if res_0[k] == res_1[k]:
                same.add(k)
            else:
                diff.add(k)
        return dict(same=same, diff=diff)

    def _judge_node_ref_consistent(var_0, var_1, part="leaf"):
        """
            计算输入的 var_0 和 var_1 中节点引用组的差异

            返回：
                {
                    "same": [[<node_name>, ...], ...],  # 两边共有的引用组，in which [<node_name>, ...] is a ref group has name id
                    "diff_0": [[<node_name>, ...], ...],  # var_0 中独有的
                    "diff_1": [[<node_name>, ...], ...],  # var_1 中独有的
                }
        """
        nodes_0 = ndl.get_nodes(var=var_0, level=-1) if part == "leaf" else _get_non_leaf_nodes(var=var_0)
        nodes_1 = ndl.get_nodes(var=var_1, level=-1) if part == "leaf" else _get_non_leaf_nodes(var=var_1)
        id_name_s_0, id_name_s_1 = defaultdict(list), defaultdict(list)
        for name, v in nodes_0:
            id_name_s_0[id(v)].append(name)
        for name, v in nodes_1:
            id_name_s_1[id(v)].append(name)
        ref_group_0 = [tuple(sorted(i)) for i in id_name_s_0.values()]
        ref_group_1 = [tuple(sorted(i)) for i in id_name_s_1.values()]
        #
        same, diff_0 = set(), set()
        for i in ref_group_0:
            if i in ref_group_1:
                same.add(i)
                ref_group_1.remove(i)
            else:
                diff_0.add(i)
        return dict(same=same, diff_0=diff_0, diff_1=set(ref_group_1))

    # 浅拷贝，保留引用 b_deepcopy=False，b_keep_internal_references=True
    """
    生成：
        {<5>
            "a": [<6>
                {<2> 1, 2, 3},
                {<3> 4, 5, 6),
                {<2> 1, 2, 3}
            ],
            "b": [<6>
                {<2> 1, 2, 3},
                {<3> 4, 5, 6),
                {<2> 1, 2, 3}
            ],
        }
    """
    x_new = ndl.copy_(var=x, b_deepcopy=False, b_keep_internal_references=True)
    # 叶节点相同（不改变引用关系）
    check_consistency(
        _judge_node_ids_consistent(var_0=x, var_1=x_new, part="leaf"),
        {'same': {':b@2', ':b@1', ':b@0', ':a@2', ':a@1', ':a@0'}, 'diff': set()}
    )
    # 结构不同，且保留引用
    check_consistency(
        _judge_node_ids_consistent(var_0=x, var_1=x_new, part="sub"),
        {'same': set(), 'diff': {':a', ':b', ''}}
    )
    check_consistency(
        _judge_node_ref_consistent(var_0=x, var_1=x_new, part="sub"),
        {'same': {('',), (':a', ':b')}, 'diff_0': set(), 'diff_1': set()}
    )

    # 浅拷贝，不保留引用 b_deepcopy=False，b_keep_internal_references=False
    """
    生成：
        {<5>
            "a": [<6>
                {<2> 1, 2, 3},
                {<3> 4, 5, 6),
                {<2> 1, 2, 3}
            ],
            "b": [<7>  # !!!
                {<2> 1, 2, 3},
                {<3> 4, 5, 6),
                {<2> 1, 2, 3}
            ],
        }
    """
    x_new = ndl.copy_(var=x, b_deepcopy=False, b_keep_internal_references=False)
    # 叶节点相同（不改变引用关系）
    check_consistency(
        _judge_node_ids_consistent(var_0=x, var_1=x_new, part="leaf"),
        {'same': {':b@2', ':b@1', ':b@0', ':a@2', ':a@1', ':a@0'}, 'diff': set()}
    )
    # 结构不同，不保留引用
    check_consistency(
        _judge_node_ids_consistent(var_0=x, var_1=x_new, part="sub"),
        {'same': set(), 'diff': {':a', ':b', ''}}
    )
    check_consistency(
        _judge_node_ref_consistent(var_0=x, var_1=x_new, part="sub"),
        {'same': {('',)}, 'diff_0': {(':a', ':b')}, 'diff_1': {(':b',), (':a',)}}
    )

    # 深拷贝，保留引用 b_deepcopy=True，b_keep_internal_references=True
    """
    生成：
        {<5>
            "a": [<6>
                {<8> 1, 2, 3},
                {<9> 4, 5, 6},
                {<8> 1, 2, 3}
            ],
            "b": [<6>
                {<8> 1, 2, 3},
                {<9> 4, 5, 6},
                {<8> 1, 2, 3}
            ],
        }
    """
    x_new = ndl.copy_(var=x, b_deepcopy=True, b_keep_internal_references=True)
    # 叶节点不相同，保留引用关系
    check_consistency(
        _judge_node_ids_consistent(var_0=x, var_1=x_new, part="leaf"),
        {'same': set(), 'diff': {':b@2', ':b@1', ':b@0', ':a@2', ':a@1', ':a@0'}}
    )
    check_consistency(
        _judge_node_ref_consistent(var_0=x, var_1=x_new, part="leaf"),
        {'same': {(':a@0', ':a@2', ':b@0', ':b@2'), (':a@1', ':b@1')}, 'diff_0': set(), 'diff_1': set()}
    )
    # 结构不同，保留引用关系
    check_consistency(
        _judge_node_ids_consistent(var_0=x, var_1=x_new, part="sub"),
        {'same': set(), 'diff': {':a', ':b', ''}}
    )
    check_consistency(
        _judge_node_ref_consistent(var_0=x, var_1=x_new, part="sub"),
        {'same': {('',), (':a', ':b')}, 'diff_0': set(), 'diff_1': set()}
    )

    # # 深拷贝，保留引用 b_deepcopy=True，b_keep_internal_references=False
    """
    生成：
        {<5>
            "a": [<6>
                {<8> 1, 2, 3},
                {<9> 4, 5, 6},
                {<8> 1, 2, 3}
            ],
            "b": [<7>  # !!!
                {<10> 1, 2, 3},  # !!!
                {<11> 4, 5, 6},  # !!!
                {<10> 1, 2, 3}  # !!!
            ],
        }
    """
    x_new = ndl.copy_(var=x, b_deepcopy=True, b_keep_internal_references=False)
    # 叶节点不相同，不保留引用关系
    check_consistency(
        _judge_node_ids_consistent(var_0=x, var_1=x_new, part="leaf"),
        {'same': set(), 'diff': {':b@2', ':b@1', ':b@0', ':a@2', ':a@1', ':a@0'}}
    )
    check_consistency(
        _judge_node_ref_consistent(var_0=x, var_1=x_new, part="leaf"),
        {'same': set(),
         'diff_0': {(':a@0', ':a@2', ':b@0', ':b@2'), (':a@1', ':b@1')},
         'diff_1': {(':a@0',), (':a@2',), (':b@0',), (':b@2',), (':a@1',), (':b@1',)}}
    )
    # 结构不同，不保留引用关系
    check_consistency(
        _judge_node_ids_consistent(var_0=x, var_1=x_new, part="sub"),
        {'same': set(), 'diff': {':a', ':b', ''}}
    )
    check_consistency(
        _judge_node_ref_consistent(var_0=x, var_1=x_new, part="sub"),
        {'same': {('',)}, 'diff_0': {(':a', ':b')}, 'diff_1': {(':b',), (':a',)}}
    )
