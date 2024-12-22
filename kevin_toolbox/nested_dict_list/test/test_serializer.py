import os
import warnings
import pytest
import torch
import numpy as np
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.data_flow.file import json_
from kevin_toolbox.utils.variable import root_dir
import kevin_toolbox.nested_dict_list as ndl
from kevin_toolbox.nested_dict_list import name_handler, serializer
from kevin_toolbox.nested_dict_list.serializer import Strictness_Level
from kevin_toolbox.computer_science.algorithm.for_dict import deep_update
from kevin_toolbox.patches.for_os import remove

temp_folder = os.path.join(os.path.dirname(__file__), "temp")
data_folder = os.path.join(os.path.dirname(__file__), "test_data")


def test_write_and_read_0():
    print("test serializer.read() and write()")

    # 基础测试，主要检查遍历、匹配流程

    var_ = {
        "a": np.random.rand(2, 5),
        "b": [torch.randn(5), torch.randn(3)],
        (1, 2, 3): (1, 2, 3),
        "model": {"name@1": "m", "paras": dict(paras=dict(layer_nums=3, input_shape=np.random.rand(2, 5)))}
    }

    # for write
    settings = [
        {"match_cond": lambda _, idx, value: "paras" == name_handler.parse_name(name=idx)[2][-1],
         "backend": (":pickle",),
         "traversal_mode": "dfs_post_order"},
        {"match_cond": "<level>-1",
         "backend": (":numpy:bin", ":torch:tensor")},
        {"match_cond":
             f'<node>{name_handler.build_name(root_node="", method_ls=[":", ":"], node_ls=["model", "name@1"])}',
         "backend": (":skip:simple",)},
        {"match_cond":
             f'<node>{name_handler.build_name(root_node="", method_ls=["@", ], node_ls=[(1, 2, 3), ])}',
         "backend": (":json",)},
        {"match_cond": lambda _, __, value: not isinstance(value, (list, dict)),
         "backend": (":skip:simple",)},
    ]
    expected_processed = [
        ["raw", {
            'a': False,
            'b': [False, False],
            (1, 2, 3): False,
            'model': {'name@1': False, 'paras': {'paras': {'layer_nums': False, 'input_shape': False}}}
        }],
        [":pickle", {
            'a': False,
            'b': [False, False],
            (1, 2, 3): False,
            'model': {'name@1': False, 'paras': {'paras': True}}
        }],
        [":numpy:bin", {
            'a': True,
            'b': [False, False],
            (1, 2, 3): False,
            'model': {'name@1': False, 'paras': {'paras': True}}
        }],
        [":torch:tensor", {
            'a': True,
            'b': [True, True],
            (1, 2, 3): False,
            'model': {'name@1': False, 'paras': {'paras': True}}
        }],
        [":skip:simple", {
            'a': True,
            'b': [True, True],
            (1, 2, 3): False,
            'model': {'name@1': True, 'paras': {'paras': True}}
        }],
        [":json", {
            'a': True,
            'b': [True, True],
            (1, 2, 3): True,
            'model': {'name@1': True, 'paras': {'paras': True}}
        }],
        [":skip:simple", {
            'a': True,
            'b': [True, True],
            (1, 2, 3): True,
            'model': {'name@1': True, 'paras': {'paras': True}}
        }]
    ]

    _hook_for_debug = dict()
    remove(temp_folder, ignore_errors=True)
    serializer.write(var=var_, output_dir=os.path.join(temp_folder, "var_"), traversal_mode="bfs",
                     b_pack_into_tar=True, settings=settings, _hook_for_debug=_hook_for_debug)
    # check
    assert len(_hook_for_debug["processed"]) == len(expected_processed)
    for (bk_name, p), (bk_name_1, p_1) in zip(_hook_for_debug["processed"], expected_processed):
        nodes = sorted(ndl.get_nodes(var=p, level=-1), key=lambda x: x[0])
        nodes_1 = sorted(ndl.get_nodes(var=p_1, level=-1), key=lambda x: x[0])
        check_consistency([i[0] for i in nodes], [i[0] for i in nodes_1])
        check_consistency([i[1] for i in nodes], [i[1] for i in nodes_1])

    # for read
    res = serializer.read(input_path=os.path.join(temp_folder, "var_.tar"))
    # check
    check_consistency(res, var_)


def test_write_and_read_1():
    print("test serializer.read() and write()")

    # 主要检查使用 ndl backend 来读取嵌套的序列化文件

    var_ = {
        "a": np.random.rand(2, 5),
        "b": [torch.randn(5), torch.randn(3)],
        (1, 2, 3): (1, 2, 3),
        "model": {"name@1": "m", "paras": dict(paras=dict(layer_nums=3, input_shape=np.random.rand(2, 5)))}
    }

    # for write
    settings = [
        {"match_cond": "<node>:model",
         "backend": (":ndl",)},
        {"match_cond": "<level>-1", "backend": (":skip:simple", ":numpy:npy", ":torch:tensor", ":pickle")},
    ]
    remove(temp_folder, ignore_errors=True)
    serializer.write(var=var_, output_dir=os.path.join(temp_folder, "var_1"), traversal_mode="bfs",
                     b_pack_into_tar=True, settings=settings)
    # check
    assert os.path.isfile(os.path.join(temp_folder, "var_1.tar"))

    # for read
    res = serializer.read(input_path=os.path.join(temp_folder, "var_1.tar"))
    # check
    check_consistency(res, var_)


def test_write_and_read_2():
    print("test serializer.read() and write()")

    # 主要检查使用 ndl backend 来读取嵌套的序列化文件（两层嵌套）

    var_ = {
        "a": np.ones([2, 5]),
        "b": [torch.as_tensor([1, 2, 3, 4]), torch.as_tensor([1, 2])],
        (1, 2, 3): (1, 2, 3),
        "model": {"name@1": "m", "paras": dict(paras=dict(layer_nums=3, input_shape=np.ones([2, 5])))}
    }

    # for read
    res = serializer.read(input_path=os.path.join(data_folder, "var_2"))
    # check
    check_consistency(res, var_)


def test_write_and_read_3():
    print("test serializer.read() and write()")

    warnings.filterwarnings("ignore", category=UserWarning)

    # 主要检查 strictness_level 中不同 level 下的表现
    # 测试模拟的情况是：无法匹配

    var_ = {
        "a": np.random.rand(2, 5),
        "b": [torch.randn(5), torch.randn(3)],
        (1, 2, 3): (1, 2, 3),
        None: None,
        "model": {"name@1": "m", "paras": dict(paras=dict(layer_nums=3, input_shape=np.random.rand(2, 5)))}
    }

    # for write
    settings = [
        {"match_cond": "<node>:model",
         "backend": (":ndl",)},
        {"match_cond": "<level>-1", "backend": (":skip:simple", ":numpy:npy")},
    ]

    for level in (Strictness_Level.COMPLETE, Strictness_Level.COMPATIBLE):
        with pytest.raises(AssertionError):
            remove(temp_folder, ignore_errors=True)
            serializer.write(var=var_, output_dir=os.path.join(temp_folder, "var_1"), traversal_mode="bfs",
                             b_pack_into_tar=True, settings=settings, strictness_level=level)

    for level in (Strictness_Level.IGNORE_FAILURE,):
        remove(temp_folder, ignore_errors=True)
        serializer.write(var=var_, output_dir=os.path.join(temp_folder, "var_1"), traversal_mode="bfs",
                         b_pack_into_tar=True, settings=settings, strictness_level=level)
        # check
        assert os.path.isfile(os.path.join(temp_folder, "var_1.tar"))

        # for read
        res = serializer.read(input_path=os.path.join(temp_folder, "var_1.tar"))
        # check
        check_consistency(res, deep_update(stem=ndl.copy_(var=var_, b_deepcopy=True), patch={"b": [None, None]}))


def test_write_and_read_4():
    print("test serializer.read() and write()")

    warnings.filterwarnings("ignore", category=UserWarning)

    # 主要检查 strictness_level 中不同 level 下的表现
    # 测试模拟的情况是：写入失败

    def func():
        class A:
            pass

        return A

    var_ = {
        "a": np.random.rand(2, 5),
        "b": [torch.randn(5), torch.randn(3)],
        (1, 2, 3): (1, 2, 3),
        None: func()()
    }

    # for write
    settings = [
        {"match_cond": "<node>:model",
         "backend": (":ndl",)},
        {"match_cond": "<level>-1", "backend": (":skip:simple", ":numpy:npy", ":torch:tensor", ":pickle")},
    ]

    for level in (Strictness_Level.COMPLETE, Strictness_Level.COMPATIBLE):
        with pytest.raises(AssertionError):
            remove(temp_folder, ignore_errors=True)
            serializer.write(var=var_, output_dir=os.path.join(temp_folder, "var_1"), traversal_mode="bfs",
                             b_pack_into_tar=True, settings=settings, strictness_level=level)

    for level in (Strictness_Level.IGNORE_FAILURE,):
        remove(temp_folder, ignore_errors=True)
        serializer.write(var=var_, output_dir=os.path.join(temp_folder, "var_1"), traversal_mode="bfs",
                         b_pack_into_tar=True, settings=settings, strictness_level=level)
        # check
        assert os.path.isfile(os.path.join(temp_folder, "var_1.tar"))

        # for read
        res = serializer.read(input_path=os.path.join(temp_folder, "var_1.tar"))
        # check
        check_consistency(res, deep_update(stem=ndl.copy_(var=var_, b_deepcopy=True), patch={None: None}))


def test_write_and_read_5():
    print("test serializer.read() and write()")

    # 测试额外指定 nodes_dir 时的写入和读取

    var_ = {
        "a": np.ones([2, 5]),
        "b": [torch.as_tensor([1, 2, 3, 4]), torch.as_tensor([1, 2])],
        (1, 2, 3): (1, 2, 3),
        "model": {"name@1": "m", "paras": dict(paras=dict(layer_nums=3, input_shape=np.ones([2, 5])))}
    }

    # for read
    json_.write(content={"kvt_dir": root_dir}, file_path="~/.kvt_cfg/.temp.json")
    res = serializer.read(input_path=os.path.join(data_folder, "var_3"))
    # check
    check_consistency(res, var_)

    # for write
    settings = [
        {"match_cond": "<node>:model", "backend": (":ndl",), "nodes_dir": f'{temp_folder}/var_2/nodes',
         "saved_node_name_format": '{hash_name}'},
        {"match_cond": "<level>-1", "backend": (":skip:simple", ":numpy:npy", ":torch:tensor", ":pickle")},
    ]
    remove(temp_folder, ignore_errors=True)
    serializer.write(var=var_, output_dir=os.path.join(temp_folder, "var_3"), traversal_mode="bfs",
                     b_pack_into_tar=False, settings=settings, strictness_level=Strictness_Level.COMPLETE)
    check_consistency(serializer.read(input_path=os.path.join(temp_folder, "var_3")), var_)
    check_consistency(
        serializer.read(input_path=os.path.join(temp_folder, "var_2", "nodes", "407c66dac7a1")),
        serializer.read(input_path=os.path.join(data_folder, "var_2", "nodes", "_model"))
    )


def test_write_and_read_keep_identical():
    print("test serializer.read() and write() at b_keep_identical_relations=True")

    a = np.array([1, 2, 3])
    b = np.ones((2, 3))
    c = [a, b]
    d = {"a": a, "b": b}
    e = {"c1": c, "c2": c}
    x = [e, a, d, c, "<same>{@1}", "<same><same>{@1}"]

    #
    remove(temp_folder, ignore_errors=True)
    serializer.write(var=x, output_dir=os.path.join(temp_folder, "var_identical"), traversal_mode="bfs",
                     b_pack_into_tar=True, b_keep_identical_relations=True)
    y = serializer.read(input_path=os.path.join(temp_folder, "var_identical.tar"))

    #
    check_consistency(x, y)
    # 检查 id 是否一致
    a_name_set, b_name_set = set(), set()
    for name, value in ndl.get_nodes(var=x, level=-1, b_strict=True):
        if value is a:
            a_name_set.add(name)
        elif value is b:
            b_name_set.add(name)
    check_consistency(*[id(ndl.get_value(var=y, name=n)) for n in a_name_set])
    check_consistency(*[id(ndl.get_value(var=y, name=n)) for n in b_name_set])
