import pytest
import os
import optuna
from kevin_toolbox.patches import for_optuna
from kevin_toolbox.data_flow.file import json_
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.computer_science.algorithm.for_nested_dict_list import get_value_by_name


def test_sample_from_feasible_domain():
    print("test for_optuna.sample_from_feasible_domain()")

    study = optuna.create_study(
        study_name="default",
        sampler=optuna.samplers.RandomSampler(seed=201),
        direction="maximize",
    )
    trial = study.ask()

    res = for_optuna.sample_from_feasible_domain(trial=trial, inputs=json_.read(
        file_path=os.path.join(os.path.dirname(__file__), "test_data", "feasible_domain_0.json")))

    check_consistency({"for_ema", "iou_thr_ls"}, set(res.keys()))
    check_consistency({":for_ema:keep_ratio", ":iou_thr_ls@0", ":iou_thr_ls@1"}, set(trial.params.keys()))

    assert isinstance(get_value_by_name(var=res, name=":for_ema:keep_ratio"), (float,))
    assert isinstance(get_value_by_name(var=res, name=":iou_thr_ls@0"), (float,))
    assert isinstance(get_value_by_name(var=res, name=":iou_thr_ls@1"), (int,))
