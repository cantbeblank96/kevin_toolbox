import copy
import pytest
import numpy as np
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.nested_dict_list import value_parser as vp


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
