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
    # 取消定时器
    set_timeout(0)

    # data_4 因为添加了额外的排除规则，不会因为 self-recursive 而产生死循环
    cls = TEST_REGISTRY_2.get(name=":class:Foo")
    assert type(cls) == type


def test_Registry_get_to_load_all():
    print("test registration.Registry.get() "
          "whether multiple loading methods can be loaded simultaneously when "
          "they appear in the same file at the same time.")
    """
        bug fix：
            - 问题：之前 get() 函数中只从 self._item_to_add 和 self._path_to_collect 中加载一次注册成员，但是加载的过程中，可能 self._item_to_add
            已经清空，但是后面因为对 self._path_to_collect 的加载，又往 self._item_to_add 中添加了待处理内容。导致不能完全加载。
            
        测试当多种加载方式同时出现在同一文件中时，能否全部同时加载。
    """
    from kevin_toolbox.computer_science.algorithm.registration.test.test_data.data_5.variable import TEST_REGISTRY_3

    temp = TEST_REGISTRY_3.get(":here:Alex")
    assert type(temp) == type
    temp = TEST_REGISTRY_3.get(":there:Bob")
    assert type(temp) == type
