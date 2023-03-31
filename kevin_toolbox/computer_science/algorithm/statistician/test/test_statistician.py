import pytest
import numpy as np
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.computer_science.algorithm.statistician import Exponential_Moving_Average
from kevin_toolbox.computer_science.algorithm.statistician.test.test_data.ema_data import inputs_ls, outputs_raw_ls, \
    outputs_unbiased_ls


@pytest.mark.parametrize("inputs, outputs_raw, outputs_unbiased",
                         zip(inputs_ls, outputs_raw_ls, outputs_unbiased_ls))
def test_Exponential_Moving_Average(inputs, outputs_raw, outputs_unbiased):
    print("test statistician.Exponential_Moving_Average")

    ema = Exponential_Moving_Average(keep_ratio=0.9, bias_correction=True)
    for i, var in enumerate(inputs):
        ema.add(var=var)
        check_consistency(ema.get(bias_correction=False), outputs_raw[i], tolerance=1e-4)
        check_consistency(ema.get(bias_correction=True), outputs_unbiased[i], tolerance=1e-4)
