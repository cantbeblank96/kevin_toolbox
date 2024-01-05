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


@pytest.mark.parametrize("build_study", [build_study_0, ])
def test_dump_and_load(build_study):
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
    check_consistency(
        *map(lambda x: {n: getattr(x, n.rsplit(":", 1)[-1], None) for n in names}, [study, study_1]))
