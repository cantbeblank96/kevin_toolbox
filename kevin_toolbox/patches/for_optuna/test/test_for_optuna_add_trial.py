import pytest
import optuna
from optuna.trial import TrialState
from unittest.mock import patch, MagicMock
from kevin_toolbox.patches.for_optuna import determine_whether_to_add_trial, enqueue_trials_without_duplicates
from kevin_toolbox.patches.for_test import check_consistency


def mock_check_consistency(a, b, **kwargs):
    """简单的字典或值相等性检查模拟"""
    return a == b


@pytest.fixture
def study():
    """创建一个内存中的 Optuna study 用于测试，每次测试前重置"""
    return optuna.create_study(study_name="test_study", storage=None)


@patch('kevin_toolbox.patches.for_test.check_consistency', side_effect=mock_check_consistency)
def test_enqueue_trials_basic(mock_check, study):
    """
    测试场景 1: 基础功能
    向一个空的 study 添加一组从未出现过的超参数
    """
    print("test enqueue_trials_without_duplicates() - Basic addition")

    # 准备数据
    hyper_paras_ls = [
        {"x": 1, "y": "a"},
        {"x": 2, "y": "b"}
    ]

    # 执行函数
    added_indices = enqueue_trials_without_duplicates(study, hyper_paras_ls)

    # 验证
    assert added_indices == [0, 1]
    assert len(study.trials) == 2
    check_consistency(study.trials[0].system_attrs["fixed_params"], hyper_paras_ls[0])
    check_consistency(study.trials[1].system_attrs["fixed_params"], hyper_paras_ls[1])

    for hyper_paras in hyper_paras_ls:
        assert not determine_whether_to_add_trial(study=study, hyper_paras=hyper_paras)

    added_indices = enqueue_trials_without_duplicates(study, hyper_paras_ls)

    assert len(added_indices) == 0


@patch('kevin_toolbox.patches.for_test.check_consistency', side_effect=mock_check_consistency)
def test_enqueue_trials_skip_duplicates(mock_check, study):
    """
    测试场景 2: 去重逻辑 (Skip Duplicates)
    如果 Study 中已经存在相同参数且状态为 COMPLETE/WAITING/RUNNING，则跳过
    """
    print("test enqueue_trials_without_duplicates() - Skip existing trials")

    # 1. 先手动向 study 添加一个已完成的 trial
    study.enqueue_trial({"x": 10})
    # 模拟运行并完成
    trial = study.ask()
    study.tell(trial, 0.9, state=TrialState.COMPLETE)

    # 2. 准备要添加的列表，其中包含一个重复项 (x=10) 和一个新项 (x=20)
    hyper_paras_ls = [
        {"x": 10},  # 应该被跳过，因为已 COMPLETE
        {"x": 20}  # 应该被添加
    ]

    # 执行
    added_indices = enqueue_trials_without_duplicates(study, hyper_paras_ls)

    # 验证
    assert added_indices == [1]  # 只有索引1 (x=20) 被添加
    assert len(study.trials) == 2  # 原有的1个 + 新增的1个
    # 确认最后加入的是 x=20
    assert study.trials[-1].user_attrs == {}  # 确保是新 trial (user_attrs为空)
    check_consistency(study.trials[-1].system_attrs["fixed_params"], hyper_paras_ls[-1])


@patch('kevin_toolbox.patches.for_test.check_consistency', side_effect=mock_check_consistency)
def test_enqueue_trials_retry_failed(mock_check, study):
    """
    测试场景 3: 失败重跑 (Retry Failed)
    如果 Study 中存在相同参数，但状态为 FAIL，默认应该允许重新添加
    """
    print("test enqueue_trials_without_duplicates() - Retry failed trials")

    # 1. 制造一个失败的 trial
    study.enqueue_trial({"lr": 0.01})
    trial = study.ask()
    try:
        raise RuntimeError("Mock Error")
    except:
        study.tell(trial, state=TrialState.FAIL)

    # 2. 尝试再次添加相同的参数
    hyper_paras_ls = [{"lr": 0.01}]

    # 执行 (默认 skip_states 不包含 FAIL)
    added_indices = enqueue_trials_without_duplicates(study, hyper_paras_ls)

    # 验证
    assert added_indices == [0]  # 应该成功添加
    assert len(study.trials) == 2  # 1个 FAIL + 1个 WAITING


@patch('kevin_toolbox.patches.for_test.check_consistency', side_effect=mock_check_consistency)
def test_enqueue_trials_custom_skip(mock_check, study):
    """
    测试场景 4: 自定义跳过状态 (Custom skip_states)
    如果将 FAIL 加入 skip_states，则失败的 trial 也不会被重试
    """
    print("test enqueue_trials_without_duplicates() - Custom skip states")

    # 1. 制造一个失败的 trial
    study.enqueue_trial({"lr": 0.01})
    trial = study.ask()
    study.tell(trial, state=TrialState.FAIL)

    # 2. 尝试添加，但指定跳过 FAIL 状态
    hyper_paras_ls = [{"lr": 0.01}]
    added_indices = enqueue_trials_without_duplicates(
        study,
        hyper_paras_ls,
        skip_states=("COMPLETE", "RUNNING", "WAITING", "FAIL")
    )

    # 验证
    assert added_indices == []  # 应该为空，没有添加
    assert len(study.trials) == 1  # 只有原来的那个 FAIL trial


@patch('kevin_toolbox.patches.for_test.check_consistency', side_effect=mock_check_consistency)
def test_enqueue_trials_internal_duplicates(mock_check, study):
    """
    测试场景 5: 输入列表内部去重
    如果输入的 list 本身包含重复项，第一个加入后变为 WAITING，第二个应该被跳过
    """
    print("test enqueue_trials_without_duplicates() - Internal duplicates in list")

    # 准备包含重复项的列表
    hyper_paras_ls = [
        {"size": 128},
        {"size": 128},  # 重复
        {"size": 256}
    ]

    # 执行
    added_indices = enqueue_trials_without_duplicates(study, hyper_paras_ls)

    # 验证
    # 第0个被添加 -> 状态 WAITING
    # 第1个检查时，发现已有 WAITING 的 trial -> 跳过
    # 第2个被添加
    assert added_indices == [0, 2]
    assert len(study.trials) == 2
