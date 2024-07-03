import os
from itertools import product
import pytest
from kevin_toolbox.data_flow.file import json_
import torch
import numpy as np
from kevin_toolbox.patches import for_os
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.computer_science.algorithm.pareto_front import get_pareto_points_idx, Optimum_Picker
from kevin_toolbox.computer_science.data_structure import Executor


def test_get_pareto_points_idx():
    print("test pareto_front.get_pareto_points_idx()")

    for _ in range(100):
        # 随机构建输入
        nums, dims = int(np.random.randint(10, 100)), int(np.random.randint(1, 10))
        directions = np.random.choice(["maximize", "minimize", "not_care"], size=dims).tolist()
        points = np.random.random([nums, dims]) - 0.5
        points = np.asarray(points)

        # 使用 get_pareto_points_idx() 求解
        pareto_idx_ls = get_pareto_points_idx(points=points, directions=directions)

        # 检验正确性
        for i, direction in enumerate(directions):
            if direction == "maximize":
                pass
            elif direction == "minimize":
                points[:, i:i + 1] *= -1
            elif direction == "not_care":
                points[:, i:i + 1] = 0
        for idx in pareto_idx_ls:
            temp = points - points[idx:idx + 1, ]
            temp[idx] -= 1
            assert np.all(np.min(temp, axis=1) < 0)


@pytest.mark.parametrize("warmup_steps, pick_per_steps", [
    (i, j) for i, j in product(range(10), range(1, 10))
])
def test_optimum_picker(warmup_steps, pick_per_steps):
    print("test pareto_front.Optimum_Picker")

    """
        模拟场景
            在训练模型时，要求比较 val_acc_1（maximize） 和 val_error_2（minimize），
            要求保存其帕累托最优时的模型。
    """

    # 一个打乱的圆的采样点序列
    metrics = torch.tensor([(-4.045084971874739, -2.9389262614623632),
                            (-3.1871199487434474, -3.852566213878947),
                            (-2.1288964578253635, 4.524135262330097),
                            (-4.648882429441257, -1.8406227634233896),
                            (-4.648882429441256, 1.8406227634233907),
                            (-0.936906572928623, 4.911436253643443),
                            (0.31395259764656414, -4.990133642141358),
                            (-4.960573506572389, 0.6266661678215226),
                            (-3.1871199487434487, 3.852566213878946),
                            (4.381533400219316, -2.4087683705085805),
                            (0.31395259764656763, 4.990133642141358),
                            (2.6791339748949827, 4.221639627510076),
                            (4.8429158056431545, -1.2434494358242767),
                            (1.5450849718747361, -4.755282581475768),
                            (4.842915805643155, 1.243449435824274),
                            (3.644843137107056, -3.422735529643445),
                            (5.0, 0.0),
                            (-2.128896457825361, -4.524135262330099),
                            (2.6791339748949836, -4.221639627510075),
                            (-4.9605735065723895, -0.6266661678215214),
                            (3.644843137107058, 3.422735529643443),
                            (4.381533400219318, 2.4087683705085765),
                            (-0.9369065729286231, -4.911436253643443),
                            (-4.045084971874736, 2.9389262614623664),
                            (1.5450849718747373, 4.755282581475767)])
    # 右下角的点是帕累托最优
    best_idx_ls = [6, 9, 12, 13, 15, 16, 18]

    temp_dir = os.path.join(os.path.dirname(__file__), "temp")
    for_os.remove(temp_dir, ignore_errors=True)

    opt_picker = Optimum_Picker(
        warmup_steps=warmup_steps, pick_per_steps=pick_per_steps,
        trigger_for_new=Executor(
            func=lambda metrics, step: json_.write(metrics.tolist(), os.path.join(temp_dir, f'{step}.json'))),
        trigger_for_out=Executor(func=lambda step, **kwargs: for_os.remove(os.path.join(temp_dir, f'{step}.json'))),
        directions=["maximize", "minimize"]
    )
    for s, v in enumerate(metrics):
        opt_picker.add(metrics=v)
        if s < warmup_steps:
            check_consistency(opt_picker.get()[1], False)
            check_consistency([i["step"] for i in opt_picker.get()[0]], list(range(s + 1)))
        elif (s-warmup_steps) % pick_per_steps == 0:
            check_consistency(opt_picker.get()[1], True)

    record_ls, b_empty_cache = opt_picker.get(b_force_clear_cache=True)
    check_consistency(b_empty_cache, True)
    check_consistency([i["step"] for i in record_ls], best_idx_ls)

    for i in range(len(metrics)):
        file_path=os.path.join(temp_dir, f'{i}.json')
        if i in best_idx_ls:
            assert os.path.isfile(file_path)
            check_consistency(
                json_.read(file_path=file_path),
                metrics[i:i+1].tolist()
            )
        else:
            assert not os.path.isfile(file_path)
