import time
import pytest
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.computer_science.data_structure import Executor
from kevin_toolbox.computer_science.algorithm.parallel_and_concurrent.utils import wrapper_with_timeout_1, \
    wrapper_with_timeout_2


def func_(i):
    if i in [2, 3, 7]:
        time.sleep(300)
    else:
        time.sleep(0.1)
    return i * 2


def test_wrapper_with_timeout():
    for wrapper in [wrapper_with_timeout_1, wrapper_with_timeout_2]:
        check_consistency(wrapper(Executor(func=func_, args=(2,)), timeout=0.3), (None, False))
        check_consistency(wrapper(Executor(func=func_, args=(1,)), timeout=0.3), (2, True))

        execution_orders = []
        completion_orders = []
        check_consistency(wrapper(Executor(func=func_, args=(2,)), timeout=0.3, _execution_orders=execution_orders,
                                  _completion_orders=completion_orders), (None, False))
        check_consistency([execution_orders, completion_orders], [[-1], []])
