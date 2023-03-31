import os
import shutil
import pickle
import pytest
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.computer_science.data_structure import Executor
from kevin_toolbox.dangerous import dump_into_pickle_with_executor_attached


def test_dump_into_pickle_with_executor_attached():
    print("test dump_into_pickle_with_executor_attached()")

    # 构建输入
    pkl_file = "./temp/egg.pkl"
    test_file = "./temp/test.txt"
    executor = Executor(func=os.system, args=[f'touch {test_file}'])
    var = {k: i for i, k in enumerate("dump_into_pickle_with_executor_attached".split("_"))}

    # 清理现场
    shutil.rmtree(f'{os.path.split(__file__)[0]}/temp', ignore_errors=True)

    # 执行
    pkl_file = f'{os.path.split(__file__)[0]}/{pkl_file}'
    dump_into_pickle_with_executor_attached(var=var, executor=executor, output_path=pkl_file)

    # 验证
    pkl_file_2 = pkl_file + ".out"
    test_file = f'{os.path.split(__file__)[0]}/{test_file}'
    assert not os.path.isfile(test_file) and os.path.isfile(pkl_file)
    os.system(
        f'cd {os.path.split(__file__)[0]};'
        f'python read_and_save_pickle.py '
        f'--input_file {pkl_file} '
        f'--output_file {pkl_file_2} '
    )
    # 检验读取后是否执行了 executor
    assert os.path.isfile(test_file)
    # 检验读取的内容
    assert os.path.isfile(pkl_file_2)
    with open(pkl_file_2, "rb") as f:
        var_2 = pickle.load(f)
    check_consistency(var, var_2)
