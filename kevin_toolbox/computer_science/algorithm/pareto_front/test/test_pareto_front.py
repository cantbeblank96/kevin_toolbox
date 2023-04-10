import pytest
import numpy as np
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.computer_science.algorithm.pareto_front import get_pareto_points_idx


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
