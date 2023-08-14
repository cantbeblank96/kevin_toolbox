import pytest
import torch
import numpy as np
from kevin_toolbox.patches.for_test import check_consistency


def test_check_consistency_0():
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


def test_check_consistency_1():
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


def test_check_consistency_2():
    print("test check_consistency() for array")

    a = torch.rand(100, 4)
    b = a.cpu().numpy()
    c = b + 1

    with pytest.raises(AssertionError):
        check_consistency(a, b, c)

    check_consistency(a, b)
