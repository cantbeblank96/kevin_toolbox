import pytest
import os
import itertools
import optuna
from kevin_toolbox.patches import for_optuna, for_os
from kevin_toolbox.data_flow.file import json_
from kevin_toolbox.patches.for_test import check_consistency
import kevin_toolbox.nested_dict_list as ndl

data_dir = os.path.join(os.path.dirname(__file__), "test_data")
temp_dir = os.path.join(os.path.dirname(__file__), "temp")

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

    assert isinstance(ndl.get_value(var=res, name=":for_ema:keep_ratio"), (float,))
    assert isinstance(ndl.get_value(var=res, name=":iou_thr_ls@0"), (float,))
    assert isinstance(ndl.get_value(var=res, name=":iou_thr_ls@1"), (int,))
    assert isinstance(ndl.get_value(var=res, name=":connection"), (int,))
    assert isinstance(ndl.get_value(var=res, name=":block_type"), (str,))


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
    assert isinstance(ndl.get_value(var=res, name=":for_ema:keep_ratio"), (float,))
    assert isinstance(ndl.get_value(var=res, name=":hhh\\:block_type"), (str,))


def test_build_storage():
    print("test for_optuna.build_storage()")

    # 测试构建 sqlite 数据库（直接使用内置库）
    for_os.remove(path=temp_dir, ignore_errors=True)
    st = for_optuna.build_storage(mode="sqlite", output_dir=temp_dir, db_name="test.db", b_clear_before_create=True)
    assert isinstance(st, optuna.storages.RDBStorage)
    assert os.path.isfile(os.path.join(temp_dir, "test.db"))

    # 测试构建 mysql 数据库（需要另外安装 pymysql 库）
    try:
        st = for_optuna.build_storage(mode="mysql", db_name="test_kevin_toolbox", b_clear_before_create=True)
        assert isinstance(st, optuna.storages.RDBStorage)
    except Exception as e:
        assert isinstance(e, ImportError)


def test_build_sampler():
    print("test for_optuna.build_sampler()")

    for n in ["optuna.samplers.GridSampler",
              "optuna.samplers.TPESampler"]:
        sampler = for_optuna.build_sampler(name=n, seed=114514,
                                           feasible_domain={"a": {"p_type": "categorical", "choices": [1, 2, 3]}})
        assert isinstance(sampler, eval(n))


def test_build_study():
    print("test for_optuna.build_study()")

    for setting_file in ["study_settings_0.json", "study_settings_1.json"]:
        p_s = json_.read(file_path=os.path.join(data_dir, setting_file))
        study = for_optuna.build_study(
            output_dir=temp_dir,
            feasible_domain_path=os.path.join(data_dir, "hyper_paras_domain.json"),
            **p_s['for_create_study']
        )
        assert isinstance(study, optuna.study.Study)


def generate_sql_study():
    for_os.remove(path=temp_dir, ignore_errors=True)
    p_s = json_.read(file_path=os.path.join(data_dir, "study_settings_1.json"))
    study = for_optuna.build_study(output_dir=temp_dir, **p_s['for_create_study'])

    def objective(trial):
        x = trial.suggest_int("x", 0, 10)
        y = trial.suggest_int("y", 0, 10)
        return (x - 2.4) ** 2, (x - y) ** 3

    study.optimize(objective, n_trials=10)

    return study, study.user_attrs["storage"], study.study_name


def generate_in_memory_study():
    study = optuna.create_study(study_name="in_memory", directions=["minimize", "maximize"], load_if_exists=True)

    def objective(trial):
        x = trial.suggest_int("x", 0, 10)
        y = trial.suggest_int("y", 0, 10)
        return (x - 2.4) ** 2, (x - y) ** 3

    study.optimize(objective, n_trials=10)

    return study, study._storage, study.study_name


def test_copy_study():
    print("test for_optuna.copy_study()")

    #
    sql_study, sql_storage, sql_study_name = generate_sql_study()
    in_study, in_storage, in_study_name = generate_in_memory_study()

    # 构建测试组合
    #   内存到 sql 数据库，内存到内存，sql 数据库到 sql 数据库 等组合
    src_ls = [
        # 内存
        dict(storage=in_storage, study_name=in_study_name),
        in_study,
        # sql db
        dict(storage=sql_storage, study_name=sql_study_name),
        dict(storage=optuna.storages.RDBStorage(sql_storage), study_name=sql_study_name)
    ]
    dst_ls = [
        # 内存
        dict(storage=None, study_name="copy"),
        dict(storage=optuna.storages.InMemoryStorage(), study_name="copy"),
        # sql db
        dict(storage=sql_storage + "copy", study_name="copy"),
        dict(storage=optuna.storages.RDBStorage(sql_storage + "copy"), study_name="copy")
    ]

    # 验证
    def get_trials(study):
        # 对于 trials，其中的 trial_id 会因为数据库种类的不同，而有不同的起始值。
        #   比如 sqlite 的 trial_id 从 0 开始，而 in_memory 的 trial_id 从 1 开始。
        #   所以在验证一致性时，我们可以先将 trial_id 去掉，然后再比较 trials。
        trials = []
        for t in study.trials:
            t = ndl.copy_(var=t.__dict__, b_deepcopy=True)
            t.pop("_trial_id")
            trials.append(t)
        return trials
    #
    for src, dst in itertools.product(src_ls, dst_ls):
        dst = for_optuna.copy_study(src=src, dst=dst, b_force=True)
        #
        src_name = src["study_name"] if isinstance(src, (dict,)) else src.study_name
        src = in_study if src_name == in_study_name else sql_study
        # 比较 directions、user_attrs、trials 是否一致
        for k in ["directions", "user_attrs"]:
            check_consistency(getattr(dst, k), getattr(src, k))
        check_consistency(get_trials(dst), get_trials(src))
