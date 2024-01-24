import os
import pytest
import optuna
import kevin_toolbox.nested_dict_list as ndl
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.patches import for_os
from kevin_toolbox.patches.for_optuna.serialize import for_study

temp_dir = os.path.join(os.path.dirname(__file__), "temp")


def build_study_0():
    def objective(trial):
        x = trial.suggest_float("x", -10, 10)
        trial.suggest_categorical(name="2", choices=["1", "2", "3"])
        kwargs = {'choices': ['1', '2', '3+3']}
        y = eval(f'trial.suggest_categorical(name=name, **kwargs)', {"trial": trial, "name": f'4', "kwargs": kwargs})
        return (x - 2) ** 2 + eval(y)

    study = optuna.create_study()
    study.optimize(objective, n_trials=5)
    return study


def build_study_1():
    def objective(trial):
        x = trial.suggest_float("x", -10, 10)
        y = trial.suggest_float("y", -10, 10)
        res = (x - 2) ** 2, y ** 3
        return res

    study = optuna.create_study(directions=["maximize", "maximize"],
                                sampler=optuna.samplers.RandomSampler(seed=114514))
    study.optimize(objective, n_trials=50)
    return study


@pytest.mark.parametrize("build_study", [build_study_0, build_study_1, ])
def test_dump_and_load_0(build_study):
    for_os.remove(path=temp_dir, ignore_errors=True)
    os.makedirs(temp_dir)

    #
    study = build_study()

    # dump
    res_s_0 = for_study.dump(study=study)

    # save
    ndl.serializer.write(var=res_s_0, output_dir=os.path.join(temp_dir, "study"), b_pack_into_tar=False)
    # read
    res_s_1 = ndl.serializer.read(input_path=os.path.join(temp_dir, "study"))

    # load
    study_1 = for_study.load(var=ndl.copy_(var=res_s_1, b_deepcopy=True))

    # dump 2nd
    res_s_2 = for_study.dump(study=study_1)

    # check
    #   只验证 dump 和 load 过程中都会保存的属性
    names = [":__dict__:study_name", ":direction", ":directions", ":user_attrs", ":trials"]
    check_consistency(
        *map(lambda x: {n: ndl.get_value(var=x, name=n, default=None) for n in names}, [res_s_0, res_s_1, res_s_2]))

    def func(x):
        # 对于某些属性直接用 getattr 会报错，因此用 try except 去获取
        nonlocal names
        out = dict()
        for n in names:
            try:
                out[n] = getattr(x, n.rsplit(":", 1)[-1], None)
            except:
                pass
        return out

    check_consistency(*map(func, [study, study_1]))


@pytest.mark.parametrize("build_study", [build_study_1, ])
def test_dump(build_study):
    print("test for_study.dump()")
    # 验证以下 bug 是否修复：
    #   - 在使用 dump() 时会意外修改 study 中的某些属性

    # 验证方法：
    #   对于方向为 "maximize" 的 study，其 best trials 中保存的是最大方向上的帕累托最优。
    #   但是若保存的过程中对 study 中的属性进行意外的替换or修改，比如将 directions 从 "maximize" 替换为序列化后的 {"value":"maximize",...}，
    #   这将会导致 study 无法正确读取 trials，此时 directions 会退回默认的 "minimize"，并对 best trials 进行修改。

    #
    study = build_study()
    best_trial_num_ls_raw = [t.number for t in study.best_trials]

    # 序列化
    res = for_study.dump(study=study)
    best_trial_num_ls_0 = [i["number"] for i in res["best_trials"]]
    #
    best_trial_num_ls_1 = [t.number for t in study.best_trials]

    check_consistency(best_trial_num_ls_raw, best_trial_num_ls_0, best_trial_num_ls_1)
