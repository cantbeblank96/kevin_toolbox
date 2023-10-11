import pytest
import numpy as np
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.patches.for_numpy import linalg


def test_softmax():
    print("test for_numpy.linalg.softmax()")

    check_consistency(
        linalg.softmax(np.asarray([0, 0.1]) * 10),
        linalg.softmax(np.asarray([0, 0.1]), temperature=0.1),
        [0.26894142, 0.73105858]
    )
    check_consistency(
        linalg.softmax(np.asarray([[[0], [0.1]]]), temperature=0.00001, axis=1),
        linalg.softmax(np.asarray([[[0], [0.1]]]), temperature=0, axis=1),
        [[[0], [1]]]
    )
    check_consistency(
        linalg.softmax(np.asarray(np.log([0.1, 0.9])) / 0.5),
        linalg.softmax(np.asarray([0.1, 0.9]), temperature=0.5, b_use_log_over_x=True),
        [0.01219512, 0.98780488]
    )
    check_consistency(
        linalg.softmax(np.asarray([[[0.1], [0.1]]]), temperature=0.00001, axis=1),
        linalg.softmax(np.asarray([[[0.1], [0.1]]]), temperature=0, axis=1),
        [[[0.5], [0.5]]]
    )
