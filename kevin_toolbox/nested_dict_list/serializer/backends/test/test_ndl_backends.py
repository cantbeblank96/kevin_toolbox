import os
import copy
import pytest
import torch
import numpy as np
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.nested_dict_list.serializer.variable import SERIALIZER_BACKEND

temp_folder = os.path.join(os.path.dirname(__file__), "temp")


def test_json():
    print("test backend :json")

    # 测试
    bk_name, node = ":json", ":1:json"
    bk = SERIALIZER_BACKEND.get(name=bk_name)(folder=temp_folder)
    x = [{123: 123, None: None, "<eval>233": 233, (2, 3, 4): (2, 3, 4)}, 233]
    # for write
    assert bk.writable(var=x)
    assert not bk.writable(var=[np.array([1, 2, 3, 4, 5]), 233])
    handle = bk.write(name=node, var=x)
    check_consistency(handle, dict(backend=bk_name, name=node))
    assert os.path.isfile(os.path.join(temp_folder, f'{node}.json'))
    # for read
    assert bk.readable(name=node)
    res = bk.read(name=node)
    check_consistency(x, res)


def test_numpy_bin():
    print("test backend :numpy:bin")

    # 测试
    bk_name, node = ":numpy:bin", ":1:numpy:bin"
    bk = SERIALIZER_BACKEND.get(name=bk_name)(folder=temp_folder)
    x = np.random.randn(100, 2)
    # for write
    assert bk.writable(var=x)
    assert not bk.writable(var=x.tolist())
    handle = bk.write(name=node, var=x)
    details = dict(shape=list(x.shape), dtype=f'{x.dtype}')
    check_consistency(handle, dict(backend=bk_name, name=node, details=details))
    assert os.path.isfile(os.path.join(temp_folder, f'{node}.bin'))
    # for read
    assert bk.readable(name=node)
    res = bk.read(name=node, details=details)
    check_consistency(x, res)


def test_numpy_npy():
    print("test backend :numpy:npy")

    # 测试
    bk_name, node = ":numpy:npy", ":1:numpy:npy"
    bk = SERIALIZER_BACKEND.get(name=bk_name)(folder=temp_folder)
    x = np.random.randn(100, 2)
    # for write
    assert bk.writable(var=x)
    assert not bk.writable(var=x.tolist())
    handle = bk.write(name=node, var=x)
    details = dict(shape=list(x.shape), dtype=f'{x.dtype}')
    check_consistency(handle, dict(backend=bk_name, name=node, details=details))
    assert os.path.isfile(os.path.join(temp_folder, f'{node}.npy'))
    # for read
    assert bk.readable(name=node)
    res = bk.read(name=node)
    check_consistency(x, res)


def test_torch_tensor():
    print("test backend :torch:tensor")

    # 测试
    bk_name, node = ":torch:tensor", ":1:torch:tensor"
    bk = SERIALIZER_BACKEND.get(name=bk_name)(folder=temp_folder)

    for device in ["cpu", "cuda"]:
        x = torch.randn([2, 3, 4], device=torch.device(device))
        # for write
        assert bk.writable(var=x)
        assert not bk.writable(var=x.detach().cpu().numpy().tolist())
        handle = bk.write(name=node, var=x)
        details = dict(shape=list(x.shape), dtype=f'{x.dtype}', device=x.device.type)
        check_consistency(handle, dict(backend=bk_name, name=node, details=details))
        assert os.path.isfile(os.path.join(temp_folder, f'{node}.pt'))
        # for read
        assert bk.readable(name=node)
        res = bk.read(name=node)
        check_consistency(x, res)


def test_torch_all():
    print("test backend :torch:all")

    # 测试
    bk_name, node = ":torch:all", ":1:torch:all"
    bk = SERIALIZER_BACKEND.get(name=bk_name)(folder=temp_folder)

    x = {"tensor": torch.randn([2, 3, 4], device=torch.device("cpu")),
         "tensor_gpu": torch.randn([2, 3, 4], device=torch.device("cuda")),
         233: [1, 2, 3, 3],
         455: np.array([1, 2, 3, 4, 5])}
    # for write
    assert bk.writable(var=x)
    handle = bk.write(name=node, var=x)
    check_consistency(handle, dict(backend=bk_name, name=node))
    assert os.path.isfile(os.path.join(temp_folder, f'{node}.pth'))
    # for read
    assert bk.readable(name=node)
    res = bk.read(name=node)
    for k in res.keys():
        check_consistency(x[k], res[k])


def test_pickle():
    print("test backend :pickle")

    # 测试
    bk_name, node = ":pickle", ":1:pickle"
    bk = SERIALIZER_BACKEND.get(name=bk_name)(folder=temp_folder)

    x = {"tensor": torch.randn([2, 3, 4], device=torch.device("cpu")),
         "tensor_gpu": torch.randn([2, 3, 4], device=torch.device("cuda")),
         233: [1, 2, 3, 3],
         455: np.array([1, 2, 3, 4, 5])}
    # for write
    assert bk.writable(var=x)
    handle = bk.write(name=node, var=x)
    check_consistency(handle, dict(backend=bk_name, name=node))
    assert os.path.isfile(os.path.join(temp_folder, f'{node}.pkl'))
    # for read
    assert bk.readable(name=node)
    res = bk.read(name=node)
    for k in res.keys():
        check_consistency(x[k], res[k])


def test_skip_simple():
    print("test backend :skip:simple")

    # 测试
    bk_name, node = ":skip:simple", ":1:skip:simple"
    bk = SERIALIZER_BACKEND.get(name=bk_name)(folder=temp_folder)

    for x in [1, 1.0, "1", (1, 1), [1, 1]]:
        # for write
        if isinstance(x, (int, float, str, tuple)):
            assert bk.writable(var=x)
            check_consistency(x, bk.write(name=bk_name, var=x))
        else:
            assert not bk.writable(var=x)
            try:
                _ = bk.write(name=bk_name, var=x)
                assert False
            except:
                assert True
        # for read
        try:
            _ = bk.read(name=node)
            assert False
        except:
            assert True


def test_skip_simple_1():
    print("test backend :skip:simple")

    # 测试
    bk_name, node = ":skip:simple", ":1:skip:simple"
    bk = SERIALIZER_BACKEND.get(name=bk_name)(folder=temp_folder)

    for x in [(1, 2, 3), (5, "d", 3.0)]:
        assert bk.writable(var=x)
    # 应该拒绝具有结构复杂的元素的 tuple
    for x in [([1, 2], 2, 3), (2, {"s": 1}), (5, "d", np.random.rand(10))]:
        assert not bk.writable(var=x)


def test_skip_all():
    print("test backend :skip:simple")

    # 测试
    bk_name, node = ":skip:all", ":1:skip:all"
    bk = SERIALIZER_BACKEND.get(name=bk_name)(folder=temp_folder)

    for x in [1, 1.0, "1", (1, 1), [1, 1]]:
        # for write
        assert bk.writable(var=x)
        check_consistency(x, bk.write(name=bk_name, var=x))
        # for read
        try:
            _ = bk.read(name=node)
            assert False
        except:
            assert True


def test_ndl():
    print("test backend :ndl")

    # 测试
    bk_name, node = ":ndl", ":1:ndl"
    bk = SERIALIZER_BACKEND.get(name=bk_name)(folder=temp_folder)

    x = {"tensor": torch.randn([2, 3, 4], device=torch.device("cpu")),
         "tensor_gpu": torch.randn([2, 3, 4], device=torch.device("cuda")),
         233: [1, 2, 3, 3],
         455: np.array([1, 2, 3, 4, 5])}
    # for write
    assert bk.writable(var=x)
    handle = bk.write(name=node, var=x)
    check_consistency(handle, dict(backend=bk_name, name=node))
    assert os.path.isfile(os.path.join(temp_folder, f'{node}.tar')) or \
           os.path.isdir(os.path.join(temp_folder, f'{node}'))
    # for read
    assert bk.readable(name=node)
    res = bk.read(name=node)
    for k in res.keys():
        check_consistency(x[k], res[k])
