import pytest
from kevin_toolbox.computer_science.algorithm.redirector import Redirectable_Sequence_Fetcher
from kevin_toolbox.computer_science.algorithm.redirector.test.test_data import Simple_Seq, Dummy_Logger
from kevin_toolbox.patches.for_test import check_consistency


def test_redirect():
    """
        测试重定向相关的基础功能
    """
    seq = Simple_Seq(data=list(range(10)), error_idx_ls=[3, 4, 5, 6])
    use_memory_after_failures = 3
    fetcher = Redirectable_Sequence_Fetcher(
        seq=seq,
        idx_redirector="increase",
        memory=-1,
        use_memory_after_failures=use_memory_after_failures,
        redirect_max_attempts=2,
        logger=Dummy_Logger()
    )

    log_for_redirect = [
        ('info', 'attempts 1：'), ('warn', 'failed to fetch 5, because of Custom Errors.'),
        ('info', 'redirected from 5 to 6.'), ('info', 'attempts 2：'),
        ('warn', 'failed to fetch 6, because of Custom Errors.'), ('info', 'redirected from 6 to 7.')
    ]

    # 记忆生效的场景
    #   访问失败索引会触发重定向
    for i in range(use_memory_after_failures):
        fetcher.logger.clear()
        check_consistency(fetcher[5], 7)  # 原始索引5失败，重定向到6，再次失败，再重定向到7，访问成功
        check_consistency(log_for_redirect, fetcher.logger.logs)
        #   同时在 memory 中进行记录
        check_consistency(
            {
                'cache': {'cache_s': {5: {'next': 6, 'failures': 1 + i, 'final': 7}, 6: {'next': 7}}}
            },
            fetcher.state_dict()['memory']
        )
    #   之后10次访问时都是直接使用记忆
    for i in range(10):
        fetcher.logger.clear()
        check_consistency(fetcher[5], 7)
        check_consistency(
            [
                ('info', 'used memory for idx=5, jump to new_idx=7.')
            ],
            fetcher.logger.logs
        )
        check_consistency(
            {
                'cache': {
                    'cache_s': {5: {'next': 6, 'failures': use_memory_after_failures - (i + 1) * 0.1, 'final': 7},
                                6: {'next': 7}}}
            },
            fetcher.state_dict()['memory']
        )
    #   记忆衰减完毕之后，若再次获取时，会重新尝试访问原始索引
    fetcher.logger.clear()
    check_consistency(fetcher[5], 7)
    check_consistency(log_for_redirect, fetcher.logger.logs)
    check_consistency(
        {
            'cache': {
                'cache_s': {5: {'next': 6, 'failures': use_memory_after_failures, 'final': 7}, 6: {'next': 7}}}
        },
        fetcher.state_dict()['memory']
    )
    #   之后10次访问时都是直接使用记忆
    for i in range(10):
        check_consistency(fetcher[5], 7)
    #   若重新尝试访问原始索引时，成功了，failures计数将会减1
    seq.error_idx_ls.pop(seq.error_idx_ls.index(5))
    fetcher.logger.clear()
    check_consistency(fetcher[5], 5)
    check_consistency(
        {
            'cache': {
                'cache_s': {5: {'next': 6, 'failures': use_memory_after_failures - 2, 'final': 7}, 6: {'next': 7}}}
        },
        fetcher.state_dict()['memory']
    )
    #   当failures计数归零时，移除该记忆
    fetcher.logger.clear()
    check_consistency(fetcher[5], 5)
    check_consistency(
        {'cache': {'cache_s': {6: {'next': 7}}}},
        fetcher.state_dict()['memory']
    )


def test_redirect_failure_with_default_value():
    """
        测试重定向失败返回默认值
    """
    seq = Simple_Seq(data=list(range(10)), error_idx_ls=[3, 4, 5, 6])
    fetcher = Redirectable_Sequence_Fetcher(
        seq=seq,
        idx_redirector="increase",
        memory=-1,
        use_memory_after_failures=3,
        redirect_max_attempts=2,
        logger=Dummy_Logger(),
        default_value="empty"
    )

    assert fetcher[3] == "empty"


def test_redirect_failure_raise_error():
    """
        测试未设置默认值时，重定向失败将抛出异常
    """
    seq = Simple_Seq(data=list(range(10)), error_idx_ls=[3, 4, 5, 6])
    fetcher = Redirectable_Sequence_Fetcher(
        seq=seq,
        idx_redirector="increase",
        memory=-1,
        use_memory_after_failures=3,
        redirect_max_attempts=2,
        logger=Dummy_Logger()
    )

    with pytest.raises(IndexError):
        temp = fetcher[3]


def test_disabled_redirect_functionality():
    """
    测试关闭重定向功能
    [6,7](@ref)
    """
    seq = Simple_Seq(data=["x"], error_idx_ls=[0])
    fetcher = Redirectable_Sequence_Fetcher(
        seq=seq,
        seq_len=1,
        redirect_max_attempts=0  # 禁用重定向
    )

    with pytest.raises(IndexError):
        temp = fetcher[0]


def test_value_checker():
    """
    """
    logger = Dummy_Logger()
    seq = Simple_Seq(data=[None, "valid"], error_idx_ls=[0])
    fetcher = Redirectable_Sequence_Fetcher(
        seq=seq,
        seq_len=2,
        logger=logger,
        value_checker=lambda x: x != "valid"
    )

    with pytest.raises(ValueError):
        temp = fetcher[0]
