import pytest
import torch
import numpy as np
from kevin_toolbox.patches.for_test import check_consistency


def test_check_consistency_for_item():
    print("test check_consistency() for single item")

    check_consistency(np.array(None, dtype=object), np.array(None, dtype=object), None)
    check_consistency(True, True)
    check_consistency(1, 1 - 1e-10, tolerance=1e-4)


def test_check_consistency_for_tuple():
    print("test check_consistency() for tuple")

    d = torch.randn(2, 2, requires_grad=True)
    e = torch.randn(3, 3, 1, requires_grad=True)
    d1 = d.clone()

    check_consistency((d, (e, e)), (d1, (e, e)))
    with pytest.raises(AssertionError):
        check_consistency((d, (e, e)), (d, (e, d)))

    check_consistency((e, e), e, require_same_shape=False)
    with pytest.raises(AssertionError):
        check_consistency((e, e), e, require_same_shape=True)

    check_consistency((d, (e, e)), (d, e), require_same_shape=False)
    with pytest.raises(AssertionError):
        check_consistency((d, (e, e)), (d, e), require_same_shape=True)

    # 仅在原始 args 中含有 np.array 或者 tensor 的情况会采取 broadcast
    for require_same_shape in [True, False]:
        with pytest.raises(AssertionError):
            check_consistency((e, e), (e,), require_same_shape=require_same_shape)
        with pytest.raises(AssertionError):
            check_consistency((d, (e, e)), (d, (e,)), require_same_shape=require_same_shape)


def test_check_consistency_for_ndl():
    print("test check_consistency() for ndl")

    a = np.array([[1, 2, 3]])
    b = np.array([[1, 2, 3]])
    c = {'d': 3, 'c': 4}
    d = {'d': 3, 'c': 4}
    check_consistency([c, a], [d, b])

    d["d"] = 10
    with pytest.raises(AssertionError):
        check_consistency([c, a], [d, b])

    d.pop("d")
    with pytest.raises(AssertionError):
        check_consistency([c, a], [d, b])


def test_check_consistency_for_array_0():
    print("test check_consistency() for array")

    a = torch.rand(100, 4)
    b = a.cpu().numpy()
    c = b + 1
    d = b + 1e-7

    with pytest.raises(AssertionError):
        check_consistency(a, b, c)

    check_consistency(a, b)
    check_consistency(a, b, d, tolerance=1e-5)

    with pytest.raises(AssertionError):
        check_consistency(a, b, d, tolerance=1e-10)


def test_check_consistency_for_array_1():
    print("test check_consistency() for array")

    a = torch.rand(100, 4)
    b = a.cpu().numpy()
    c = b + 1

    with pytest.raises(AssertionError):
        check_consistency(a, b, c)

    check_consistency(a, b)


def test_check_consistency_for_broadcast():
    print("test check_consistency() for broadcast")

    """
    测试 require_same_shape 取不同值时，对于不同种类输入的形状检查能力和 broadcast 能力
    """
    a = np.array([[1, 2, 3]])
    b = torch.tensor([1, 2, 3], dtype=torch.float32, requires_grad=True)
    e = (1, 2, 3)
    c = {'d': 3, 'c': 4}

    # 令 require_same_shape=False，且含有 np.array 或者 tensor 元素，则会进行 broadcast 操作
    check_consistency(a, b, e, require_same_shape=False)
    # 令 require_same_shape=True，此时形状不一致会报错
    check_consistency(b, e, require_same_shape=True)
    with pytest.raises(AssertionError):
        check_consistency(a, b, e, require_same_shape=True)
    # 当输入中不含有 np.array 或者 tensor 元素，无论 require_same_shape 取何值，都不进行 broadcast 操作
    check_consistency(np.array((e, e)), e, require_same_shape=False)
    for require_same_shape in [True, False]:
        with pytest.raises(AssertionError):
            check_consistency((e, e), e, require_same_shape=require_same_shape)
        with pytest.raises(AssertionError):
            check_consistency([(e, e)], [e], require_same_shape=require_same_shape)

    # 特殊情况
    check_consistency(np.array([[]], dtype=object), np.array([], dtype=int), require_same_shape=False)
    with pytest.raises(AssertionError):
        check_consistency(np.array([[]], dtype=object), np.array([], dtype=int), require_same_shape=True)
    with pytest.raises(AssertionError):
        check_consistency(np.array([[]], dtype=object), tuple(), require_same_shape=True)


def test_check_consistency_for_nan():
    print("test check_consistency() for np.nan")

    """
    应该将不同 array 中相同位置的 np.nan 视为相等
    """
    check_consistency(np.nan, np.nan)

    check_consistency(np.array([[np.nan, np.nan, 3]]), np.array([np.nan, np.nan, 3]), require_same_shape=False)
    check_consistency(np.array([[np.nan, np.nan],
                                [np.nan, np.nan]]), np.nan, np.array([np.nan, ]), require_same_shape=False)

    with pytest.raises(AssertionError):
        check_consistency(np.array([[np.nan, np.nan, 3]]), np.nan, require_same_shape=False)
    with pytest.raises(AssertionError):
        check_consistency(np.array([[np.nan, np.nan, 3]]), np.array([[np.nan, 2, 3]]))
