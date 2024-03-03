import os
import signal
import pytest

"""
用于测试 Registry 的健壮性，亦即应对特殊情况是否能够正确报错
"""


# 设置信号处理函数
def set_timeout(seconds):
    """
        计时器
            - 不阻塞原进程
            - 超时抛出错误
    """

    def timeout_handler(signum, frame):
        raise TimeoutError("Timeout!")

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)


def test_Registry_collect_from_paths_avoid_infinite_loop_due_to_self_recursive_call():
    print("test registration.Registry.collect_from_paths() "
          "whether infinite loops caused by self-recursive calls can be avoided.")
    """
        测试对于，因为自我递归调用而产生死循环的情况，是否能及时报错
    """
    from kevin_toolbox.computer_science.algorithm.registration.test.test_data.data_3.variable import TEST_REGISTRY
    from kevin_toolbox.computer_science.algorithm.registration.test.test_data.data_4.variable import TEST_REGISTRY_2

    # data_3 会因为 self-recursive 而产生死循环
    with pytest.raises(RuntimeError):
        # 如果产生死循环，则会由定时器抛出 TimeoutError 异常
        # 否则由 TEST_REGISTRY 抛出 RuntimeError 异常
        set_timeout(10)
        # import time; time.sleep(4)
        cls = TEST_REGISTRY.get(name=":class:Foo")
        assert type(cls) == type

    # data_4 因为添加了额外的排除规则，不会因为 self-recursive 而产生死循环
    cls = TEST_REGISTRY_2.get(name=":class:Foo")
    assert type(cls) == type
