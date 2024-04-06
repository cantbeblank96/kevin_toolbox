import copy
import pytest
import numpy as np
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.nested_dict_list import value_parser as vp
from kevin_toolbox.nested_dict_list import get_nodes, get_value, copy_


def test_all_0():
    x = {
        "model": {
            "head": {
                "input_shape": [64, 3, "<v>{cfg:dataset:image_size@0}", "<v>{cfg:dataset:image_size@1}"],
                "output_shape": "[16]+<v>{cfg:model:head:input_shape}[1:]",
            }
        },
        "dataset": {
            # "name": "<v>{cfg:dataset:name}",
            "batch_size": "<v>{cfg:model:head:input_shape@0}",
            "image_size": ["<eval>110", 96],
        },
    }
    raw_x = copy.deepcopy(x)

    print("test value_parser.parse_references()")
    node_s = vp.parse_references(
        var=x,
        flag="v"
    )
    check_consistency(
        {':model:head:input_shape@3': {'expression': 'p_0', 'paras': {'p_0': 'cfg:dataset:image_size@1'}},
         ':model:head:input_shape@2': {'expression': 'p_0', 'paras': {'p_0': 'cfg:dataset:image_size@0'}},
         ':model:head:output_shape': {'expression': '[16]+p_0[1:]', 'paras': {'p_0': 'cfg:model:head:input_shape'}},
         ':dataset:batch_size': {'expression': 'p_0', 'paras': {'p_0': 'cfg:model:head:input_shape@0'}}},
        node_s
    )

    print("test value_parser.cal_relation_between_references()")

    node_s, b_is_DAG, order = vp.cal_relation_between_references(node_s=node_s, b_verbose=False)

    check_consistency(b_is_DAG, True)
    check_consistency(
        {':model:head:input_shape@3': {'expression': 'p_0', 'paras': {'p_0': 'cfg:dataset:image_size@1'},
                                       'upstream_node': set(), 'downstream_node': {':model:head:output_shape'}},
         ':model:head:input_shape@2': {'expression': 'p_0', 'paras': {'p_0': 'cfg:dataset:image_size@0'},
                                       'upstream_node': set(), 'downstream_node': {':model:head:output_shape'}},
         ':model:head:output_shape': {'expression': '[16]+p_0[1:]', 'paras': {'p_0': 'cfg:model:head:input_shape'},
                                      'upstream_node': {':model:head:input_shape@2', ':model:head:input_shape@3'},
                                      'downstream_node': set()},
         ':dataset:batch_size': {'expression': 'p_0', 'paras': {'p_0': 'cfg:model:head:input_shape@0'},
                                 'upstream_node': set(), 'downstream_node': set()}},
        node_s
    )
    check_consistency(":model:head:output_shape", order[-1])

    print("test value_parser.eval_references()")
    # 将被引用节点 "image_size@0": "<eval>110" 的值替换为 110
    vp.eval_references(var=x, node_s=node_s, order=order,
                       converter_for_ref=lambda idx, v: eval(v[6:]) if isinstance(v, (str,)) and v.startswith(
                           "<eval>") else v)
    check_consistency(
        {'model': {'head': {'input_shape': [64, 3, 110, 96], 'output_shape': [16, 3, 110, 96]}},
         'dataset': {'batch_size': 64, 'image_size': [110, 96]}},
        x
    )

    print("test value_parser.parse_and_eval_references()")
    raw_x, name_ls = vp.parse_and_eval_references(
        var=raw_x,
        flag="v",
        converter_for_ref=lambda idx, v: eval(v[6:]) if isinstance(v, (str,)) and v.startswith(
            "<eval>") else v
    )
    check_consistency(raw_x, x)
    check_consistency(name_ls, order)


def test_all_1():
    x = {
        "model": {
            "head": {
                "input_shape": [64, 3, "<v>{cfg:dataset:image_size@0}", "<v>{cfg:dataset:image_size@1}"],
                "output_shape": "[16]+<v>{cfg:model:head:input_shape}[1:]",
            }
        },
        "dataset": {
            "name": "<v>{cfg:dataset:name}",
            "batch_size": "<v>{cfg:model:head:input_shape@0}",
            "image_size": [110, 96],
        },
    }
    raw_x = copy.deepcopy(x)

    print("test value_parser.parse_references()")
    node_s = vp.parse_references(
        var=x,
        flag="v"
    )
    check_consistency(
        {':model:head:input_shape@3': {'expression': 'p_0', 'paras': {'p_0': 'cfg:dataset:image_size@1'}},
         ':model:head:input_shape@2': {'expression': 'p_0', 'paras': {'p_0': 'cfg:dataset:image_size@0'}},
         ':model:head:output_shape': {'expression': '[16]+p_0[1:]', 'paras': {'p_0': 'cfg:model:head:input_shape'}},
         ':dataset:name': {'expression': 'p_0', 'paras': {'p_0': 'cfg:dataset:name'}},
         ':dataset:batch_size': {'expression': 'p_0', 'paras': {'p_0': 'cfg:model:head:input_shape@0'}}},
        node_s
    )

    print("test value_parser.cal_relation_between_references()")

    node_s, b_is_DAG, order = vp.cal_relation_between_references(node_s=node_s, b_verbose=True)
    check_consistency(b_is_DAG, False)
    check_consistency(order, None)
    check_consistency(
        {':model:head:input_shape@3': {'expression': 'p_0', 'paras': {'p_0': 'cfg:dataset:image_size@1'},
                                       'upstream_node': set(), 'downstream_node': {':model:head:output_shape'}},
         ':model:head:input_shape@2': {'expression': 'p_0', 'paras': {'p_0': 'cfg:dataset:image_size@0'},
                                       'upstream_node': set(), 'downstream_node': {':model:head:output_shape'}},
         ':model:head:output_shape': {'expression': '[16]+p_0[1:]', 'paras': {'p_0': 'cfg:model:head:input_shape'},
                                      'upstream_node': {':model:head:input_shape@2', ':model:head:input_shape@3'},
                                      'downstream_node': set()},
         ':dataset:name': {'expression': 'p_0', 'paras': {'p_0': 'cfg:dataset:name'},
                           'upstream_node': {':dataset:name'}, 'downstream_node': {':dataset:name'}},
         ':dataset:batch_size': {'expression': 'p_0', 'paras': {'p_0': 'cfg:model:head:input_shape@0'},
                                 'upstream_node': set(), 'downstream_node': set()}},
        node_s
    )


def test_replace_identical_with_reference():
    flag = "same"

    a = np.array([1, 2, 3])
    b = np.ones((2, 3))
    c = [a, b]
    d = {"a": a, "b": b}
    e = {"c1": c, "c2": c}
    x = [e, a, d, c, "<same>{@1}", "<same><same>{@1}"]

    # 经过替换后，整个结构中仅有一个 a\b 和若干个引用
    y = vp.replace_identical_with_reference(var=copy_(x, b_deepcopy=False), flag=flag)
    #
    a_name_set, b_name_set = set(), set()
    for name, value in get_nodes(var=y, level=-1, b_strict=True):
        if value is a:
            a_name_set.add(name)
        elif value is b:
            b_name_set.add(name)
    assert len(a_name_set) == 1 and len(b_name_set) == 1
    a_name = a_name_set.pop()
    b_name = b_name_set.pop()
    #
    for name, value in get_nodes(var=y, level=-1, b_strict=True):
        if isinstance(value, str):
            if value == f'<{flag}>{{{a_name}}}':
                check_consistency(get_value(var=x, name=name), a)
            elif value == f'<{flag}>{{{b_name}}}':
                check_consistency(get_value(var=x, name=name), b)

    # 恢复原状 1
    x1 = vp.replace_identical_with_reference(var=copy_(y, b_deepcopy=False), flag=flag, b_reverse=True)

    # 恢复原状 2
    x2 = vp.replace_identical_with_reference(
        var=[{'c1': [a, '<same>{@2:b}'], 'c2': '<same>{@0:c1}'}, '<same>{@0:c1@0}',
             {'a': '<same>{@0:c1@0}', 'b': b}, '<same>{@0:c1}', '<same><same>{@1}', '<same><same><same>{@1}'],
        flag=flag, b_reverse=True
    )

    # 检查 id 是否一致
    check_consistency(x, x1, x2)
    for name, value in get_nodes(var=x, level=-1, b_strict=True):
        if value is a or value is b:
            check_consistency(id(a if value is a else b), id(get_value(var=x1, name=name)),
                              id(get_value(var=x2, name=name)))
