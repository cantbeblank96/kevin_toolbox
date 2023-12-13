import pytest
import os
import optuna
from kevin_toolbox.patches import for_optuna
from kevin_toolbox.data_flow.file import json_
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.nested_dict_list import get_value

data_dir = os.path.join(os.path.dirname(__file__), "test_data")
study = optuna.create_study(
    study_name="default",
    sampler=optuna.samplers.RandomSampler(seed=201),
    direction="maximize",
)


def test_sample_from_feasible_domain_0():
    print("test for_optuna.sample_from_feasible_domain()")

    trial = study.ask()

    res, name_ls = for_optuna.sample_from_feasible_domain(trial=trial, var=json_.read(
        file_path=os.path.join(data_dir, "feasible_domain_0.json")))

    check_consistency({"for_ema", "iou_thr_ls", "connection", "block_type"}, set(res.keys()))
    check_consistency({":for_ema:keep_ratio", ":iou_thr_ls@0", ":iou_thr_ls@1", ":connection", ":block_type"},
                      set(trial.params.keys()), set(name_ls))

    assert isinstance(get_value(var=res, name=":for_ema:keep_ratio"), (float,))
    assert isinstance(get_value(var=res, name=":iou_thr_ls@0"), (float,))
    assert isinstance(get_value(var=res, name=":iou_thr_ls@1"), (int,))
    assert isinstance(get_value(var=res, name=":connection"), (int,))
    assert isinstance(get_value(var=res, name=":block_type"), (str,))


def test_sample_from_feasible_domain_1():
    print("test for_optuna.sample_from_feasible_domain()")

    trial = study.ask()

    res, node_vs_paras_s = for_optuna.sample_from_feasible_domain(
        trial=trial, var=json_.read(file_path=os.path.join(data_dir, "feasible_domain_1.json")),
        f_p_name_builder=lambda idx, p_type: f"<{p_type}>{idx}",
        b_use_name_as_idx=False
    )

    check_consistency({"keep_ratio", "<categorical>hhh:block_type"}, set(node_vs_paras_s.values()),
                      set(trial.params.keys()))
    assert isinstance(get_value(var=res, name=":for_ema:keep_ratio"), (float,))
    assert isinstance(get_value(var=res, name=":hhh\\:block_type"), (str,))
