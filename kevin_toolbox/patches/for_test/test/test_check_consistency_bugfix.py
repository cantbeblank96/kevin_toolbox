import pytest
import torch
import numpy as np
from kevin_toolbox.patches.for_test import check_consistency


def test_check_consistency_0():
    print("test check_consistency()")

    a = np.array([[1, 2, 3]])
    b = np.array([[1, 2, 3]])
    c = {'d': 3, 'c': 4}

    check_consistency([c, a], [c, b])
    np.array_equal(np.array([c, a]), np.array([c, b]))
    for require_same_shape in [True, False]:
        with pytest.raises(AssertionError):
            check_consistency(np.array([c, a]), np.array([c, ]), require_same_shape=require_same_shape)
        with pytest.raises(AssertionError):
            check_consistency(np.array([[]]), a, require_same_shape=require_same_shape)

    check_consistency(np.array([["None", None, a]], dtype=object), ("None", None, a),
                      require_same_shape=False)


def test_check_consistency_1():
    print("test check_consistency()")

    check_consistency(np.array([[]], dtype=int), np.array([], dtype=int), require_same_shape=False)
    with pytest.raises(AssertionError):
        check_consistency(np.array([[]], dtype=int), np.array([], dtype=int), require_same_shape=True)

    check_consistency(np.array([], dtype=int), np.array([], dtype=int), require_same_shape=True)
