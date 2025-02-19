import time
import pytest
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.computer_science.data_structure import Executor
from kevin_toolbox.computer_science.algorithm import parallel_and_concurrent as pc


def func_(i):
    if i in [2, 3, 7]:
        time.sleep(0.5)
    else:
        time.sleep(0.1)
    return i * 2


def test_multi_thread_and_process_execute_0():
    """
        测试无 timeout 时的并行

        当 最大线程/进程数为 5 时，
          首先分配5个线程/进程去执行 0、1、2、3、4 任务，
          其中任务 2、3 由于等待时间较长而驻留，剩余3个任务结束后，其对应线程/进程执行后续的 5、6、7 任务
          其中任务 7 由于等待时间较长而驻留，剩余2个任务结束后，对应线程/进程继续执行 8、9 任务
          最后 2、3 和 7 任务执行完毕、对应线程/进程释放。

        时序表为：
                  0 ~~~~ 0.1 ~~~~ 0.2 ~~~~~~~ 0.5 ~~~~ 0.6
          0,1,4:  [-------]
          2,3:    [---------------------------]
          5,6:            [-------]
          7:              [----------------------------]
          8,9:                    [-------]
    """
    for multi_execute in [pc.multi_thread_execute, pc.multi_process_execute]:
        hook_for_debug = dict()
        res_ls, failed_idx_ls = multi_execute(executors=[Executor(func=func_, args=(i,)) for i in range(10)],
                                              worker_nums=5, _hook_for_debug=hook_for_debug)
        check_consistency([i * 2 for i in range(10)], res_ls)
        check_consistency([], failed_idx_ls)
        #
        check_consistency([0, 1, 2, 3, 4], sorted(hook_for_debug['execution_orders'][:5]))
        check_consistency([5, 6, 7], sorted(hook_for_debug['execution_orders'][5:8]))
        check_consistency([8, 9], sorted(hook_for_debug['execution_orders'][8:]))
        #
        check_consistency([0, 1, 4], sorted(hook_for_debug['completion_orders'][:3]))
        check_consistency([5, 6], sorted(hook_for_debug['completion_orders'][3:5]))
        check_consistency([8, 9], sorted(hook_for_debug['completion_orders'][5:7]))
        check_consistency([2, 3], sorted(hook_for_debug['completion_orders'][7:9]))
        check_consistency([7, ], sorted(hook_for_debug['completion_orders'][9:]))


def func_2(i):
    # 模拟部分任务长时间运行，部分任务正常结束
    if i in [2, 3, 7]:
        time.sleep(100)
    else:
        time.sleep(0.1)
    return i * 2


def test_multi_thread_and_process_execute_1():
    """
        测试有 timeout 时的并行
    """
    for multi_execute in [pc.multi_thread_execute, pc.multi_process_execute]:
        for worker_nums, expected_time in [(1, 1.4), (2, 0.8), (5, 0.4), (10, 0.3)]:
            hook_for_debug = dict()
            a = time.time()
            res_ls, failed_idx_ls = multi_execute(
                executors=[Executor(func=func_2, args=(i,)) for i in range(10)], timeout=0.3,
                worker_nums=worker_nums, _hook_for_debug=hook_for_debug)
            gap = time.time() - a
            #
            check_consistency([0, 2, None, None, 8, 10, 12, None, 16, 18], res_ls)
            check_consistency([2, 3, 7], failed_idx_ls)
            #
            assert expected_time <= gap <= max(expected_time + 0.5, expected_time * 1.5)
            # 执行顺序
            if worker_nums == 1:
                """
                    当 线程/进程数为 1 时，        
                    时序表为：
                              0 ~~~ 0.1 ~~~ 0.2 ~~~ 0.5 ~~~ 0.8 ~~ 0.9 ~~~ 1.0 ~~ 1.1 ~~~ 1.2 ~~~ 1.3 ~~~ 1.4
                              [--0---][---1--][---2--x[--3--x[---4--][---5--][--6--][---7--x[---8--][---9--]
                """
                check_consistency(list(range(10)), hook_for_debug['execution_orders'])
                check_consistency(list(i for i in range(10) if i not in [2, 3, 7]),
                                  hook_for_debug['completion_orders'])
            elif worker_nums == 2:
                """
                    当 线程/进程数为 2 时，
                    时序表为：
                              0 ~~~ 0.1  ~~~ 0.4  ~~~ 0.5 ~~~ 0.6  ~~~ 0.7  ~~~ 0.8
                      0,1:    [-------]
                      2,3:            [--------x
                      4,5:                     [-------]
                      6,8,9:                           [---6---][---8---][---9---]
                      7:                               [-------------------------x
                """
                #
                check_consistency([0, 1], sorted(hook_for_debug['execution_orders'][:2]))
                check_consistency([2, 3], sorted(hook_for_debug['execution_orders'][2:4]))
                check_consistency([4, 5], sorted(hook_for_debug['execution_orders'][4:6]))
                check_consistency([6, 7], sorted(hook_for_debug['execution_orders'][6:8]))
                check_consistency([8, 9], hook_for_debug['execution_orders'][8:])
                #
                check_consistency([0, 1], sorted(hook_for_debug['completion_orders'][:2]))
                check_consistency([4, 5], sorted(hook_for_debug['completion_orders'][2:4]))
                check_consistency([6, 8, 9], hook_for_debug['completion_orders'][4:])
            elif worker_nums == 5:   # 该设置下完成顺序有一定概率不确定因此不进行检查
                """
                    当 线程/进程数为 5 时，        
                    时序表为：
                              0 ~~~ 0.1  ~~~ 0.2  ~~~ 0.3  ~~~ 0.4
                      0,1,4:  [-------]
                      2,3:    [------------------------x
                      5,6:            [-------]
                      7:              [-------------------------x
                      8,9:                    [-------]
                """
                #
                check_consistency([0, 1, 2, 3, 4], sorted(hook_for_debug['execution_orders'][:5]))
                check_consistency([5, 6, 7], sorted(hook_for_debug['execution_orders'][5:8]))
                check_consistency([8, 9], sorted(hook_for_debug['execution_orders'][8:]))
                # #
                # check_consistency([0, 1, 4], sorted(hook_for_debug['completion_orders'][:3]))
                # check_consistency([5, 6], sorted(hook_for_debug['completion_orders'][3:5]))
                # check_consistency([8, 9], sorted(hook_for_debug['completion_orders'][5:]))
                pass
            elif worker_nums == 10:
                """
                    当 线程/进程数为 10 时，        
                    时序表为：
                              0 ~~~ 0.1  ~~~ 0.3
                      ^2,3,7: [-------]
                      2,3,7:  [----------------x
                """
                check_consistency(list(range(10)), sorted(hook_for_debug['execution_orders']))
                check_consistency(list(i for i in range(10) if i not in [2, 3, 7]),
                                  sorted(hook_for_debug['completion_orders']))
