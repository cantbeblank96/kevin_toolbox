import random
import pytest
import torch
import numpy as np
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.computer_science.algorithm.statistician import Exponential_Moving_Average, Average_Accumulator, \
    Accumulator_for_Ndl
from kevin_toolbox.computer_science.algorithm.statistician.test.test_data.ema_data import inputs_ls, outputs_raw_ls, \
    outputs_unbiased_ls


@pytest.mark.parametrize("inputs, outputs_raw, outputs_unbiased",
                         zip(inputs_ls, outputs_raw_ls, outputs_unbiased_ls))
def test_Exponential_Moving_Average(inputs, outputs_raw, outputs_unbiased):
    print("test statistician.Exponential_Moving_Average")

    ema = Exponential_Moving_Average(keep_ratio=0.9, bias_correction=True)
    # 基础功能测试
    for i, var in enumerate(inputs):
        ema.add(var=var)
        check_consistency(ema.get(bias_correction=False), outputs_raw[i], tolerance=1e-4)
        check_consistency(ema.get(bias_correction=True), outputs_unbiased[i], tolerance=1e-4)
    ema.clear()

    # 测试保存、加载状态
    break_it = random.randint(1, len(inputs) - 1)
    for i in range(0, break_it):
        ema.add(var=inputs[i])
    state_s = ema.state_dict()
    #
    ema.clear()
    ema_new = Exponential_Moving_Average(keep_ratio=0.9, bias_correction=True)
    #
    ema_new.load_state_dict(state_dict=state_s)
    ema.load_state_dict(state_dict=state_s)
    for i in range(break_it, len(inputs)):
        for it in [ema, ema_new]:
            it.add(var=inputs[i])
            check_consistency(it.get(bias_correction=False), outputs_raw[i], tolerance=1e-4)
            check_consistency(it.get(bias_correction=True), outputs_unbiased[i], tolerance=1e-4)


def test_Average_Accumulator_0():
    print("test statistician.Average_Accumulator")

    # 基础功能测试
    avg = Average_Accumulator()
    check_consistency(None, avg.get())

    for _ in range(10):
        avg.clear()
        x_ls = torch.randn(100)
        avg = Average_Accumulator()
        avg.add_sequence(x_ls)
        check_consistency(torch.mean(x_ls), avg.get())

    # 测试保存、加载状态
    for _ in range(10):
        avg.clear()
        x_ls = torch.randn(100)
        #
        break_it = random.randint(1, len(x_ls) - 1)
        avg.add_sequence(x_ls[:break_it])
        #
        state_s = avg.state_dict()
        #
        avg.clear()
        avg_new = Average_Accumulator()
        avg_new.load_state_dict(state_dict=state_s)
        avg.load_state_dict(state_dict=state_s)
        #
        avg.add_sequence(x_ls[break_it:])
        avg_new.add_sequence(x_ls[break_it:])
        #
        check_consistency(torch.mean(x_ls), avg.get(), avg_new.get())


def test_Average_Accumulator_1():
    print("test statistician.Average_Accumulator")

    # 测试带权重的平均值
    avg = Average_Accumulator()

    count_v, count_w = np.zeros([3, 3]), 0
    for _ in range(10):
        v, w = np.random.rand(*count_v.shape), random.random()
        avg.add(var=v, weight=w)
        count_v += v * w
        count_w += w
    check_consistency(count_v / count_w, avg.get())


def test_Accumulator_for_Ndl():
    print("test statistician.Accumulator_for_Ndl")

    worker = Accumulator_for_Ndl(accumulator_builder=Average_Accumulator)

    worker.add({
        1: 2.1,
        "233": torch.ones(10),
        "543": [
            np.array([1, 2, 3]),
            np.array([4, 5, 6]),
        ]
    }, weight=0.8)

    worker.add({
        1: 3.1,
        "233": torch.zeros(10),
        "543": [
            np.array([0, 2, 3]),
            np.array([0, 5, 6]),
        ]
    }, weight=1.4)

    check_consistency(
        worker.get(),
        {
            1: 6.02 / 2.2,
            "233": torch.ones(10) * 0.36363637,
            "543": [
                np.array([0.36363636, 2., 3.]),
                np.array([1.45454545, 5., 6.]),
            ]
        }
    )
