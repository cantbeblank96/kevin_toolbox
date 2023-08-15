import time
import pytest
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.computer_science.data_structure import Executor
from kevin_toolbox.computer_science.algorithm import parallel_and_concurrent as pc


def test_multi_thread_execute():
    print("test parallel_and_concurrent.multi_thread_execute()")

    # 当 最大线程数为 5 时，
    #   首先分配5个线程去执行 0、1、2、3、4 任务，
    #   其中任务 2、3 由于等待时间较长而驻留，剩余3个任务结束后，其对应线程执行后续的 5、6、7 任务
    #   其中任务 7 由于等待时间较长而驻留，剩余2个任务结束后，对应线程继续执行 8、9 任务
    #   最后 2、3 和 7 任务执行完毕、对应线程释放。
    # 时序表为：
    #           0 ~~~ 0.01 ~~~ 0.02 ~~~~~~ 0.05 ~~~ 0.06
    #   0,1,4:  [-------]
    #   2,3:    [---------------------------]
    #   5,6:            [-------]
    #   7:              [----------------------------]
    #   8,9:                    [-------]
    def func_(i):
        if i in [2, 3, 7]:
            time.sleep(0.05)
        else:
            time.sleep(0.01)
        return i * 2

    hook_for_debug = dict()
    res_ls, failed_idx_ls = pc.multi_thread_execute(executors=[Executor(func=func_, args=(i,)) for i in range(10)],
                                                    thread_nums=5, _hook_for_debug=hook_for_debug)
    check_consistency([i * 2 for i in range(10)], res_ls)
    check_consistency(
        {
            'execution_orders': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            'completion_orders': [0, 1, 4, 5, 6, 8, 9, 2, 3, 7]
        },
        hook_for_debug
    )
