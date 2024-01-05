import os
import pytest
import optuna
import kevin_toolbox.nested_dict_list as ndl
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.patches import for_os
from kevin_toolbox.patches.for_optuna.serialize import for_trial

temp_dir = os.path.join(os.path.dirname(__file__), "temp")


def build_trials_0():
    def objective(trial):
        x = trial.suggest_float("x", -10, 10)
        trial.suggest_categorical(name="2", choices=["1", "2", "3"])
        kwargs = {'choices': ['1', '2', '3+3']}
        y = eval(f'trial.suggest_categorical(name=name, **kwargs)', {"trial": trial, "name": f'4', "kwargs": kwargs})
        return (x - 2) ** 2 + eval(y)

    study = optuna.create_study()
    study.optimize(objective, n_trials=5)
    return study.get_trials()


def build_trials_1():
    def objective(trial):
        x = trial.suggest_float("x", -10, 10)
        trial.suggest_categorical(name="2", choices=["1", "2", "3"])
        y = eval(f'trial.suggest_categorical(name, kwargs)', {"trial": trial, "name": f'4', "kwargs": [1, 2, 3]})
        return (x - 2) ** 2, x + y

    study = optuna.create_study(directions=["maximize", "minimize"])
    study.optimize(objective, n_trials=5)
    return study.get_trials()


@pytest.mark.parametrize("build_trials", [build_trials_0, build_trials_1])
def test_dump_and_load(build_trials):
    for_os.remove(path=temp_dir, ignore_errors=True)
    os.makedirs(temp_dir)

    #
    trial_ls = build_trials()

    # dump
    res_ls_0 = [for_trial.dump(trial=trial) for trial in trial_ls]

    # save
    ndl.serializer.write(var=res_ls_0, output_dir=os.path.join(temp_dir, "trials"), b_pack_into_tar=False)
    # read
    res_ls_1 = ndl.serializer.read(input_path=os.path.join(temp_dir, "trials"))

    # load
    trial_ls_1 = [for_trial.load(var=i) for i in ndl.copy_(var=res_ls_1, b_deepcopy=True)]

    # dump 2nd
    res_ls_2 = [for_trial.dump(trial=trial) for trial in trial_ls_1]

    # check
    check_consistency(res_ls_0, res_ls_1, res_ls_2)
    check_consistency(trial_ls, trial_ls_1)
