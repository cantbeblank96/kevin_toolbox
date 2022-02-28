"""
测试整体矩阵乘法与分块矩阵乘法的一致性
"""
import numpy as np
import torch

# seed = 1515
# seed = 0

if __name__ == '__main__':
    for seed in range(10000):
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

        print("构造测试数据")
        feature = np.random.uniform(0, 1, [2, 256]).astype(np.float32)

        feature_outer_i = torch.tensor(feature[0], device=torch.device('cuda'),
                                       dtype=torch.float32)
        feature_outer_j = torch.tensor(feature[1], device=torch.device('cuda'),
                                       dtype=torch.float32)
        feature = torch.tensor(feature, device=torch.device('cuda'),
                               dtype=torch.float32)
        # feature_outer_i = patch_for_torch.Tensor(feature[0])
        # feature_outer_j = patch_for_torch.Tensor(feature[1])
        # feature = patch_for_torch.Tensor(feature)
        print("检查块数据与整体数据的一致性")
        print(f"same? {feature[0] == feature_outer_i}  {feature[1] == feature_outer_j}")

        # 分块乘法
        a = feature_outer_j.matmul(feature_outer_i.t()).unsqueeze(-1)
        print(f"elem in [0,1] cal by block: {a[0].cpu().numpy()}")

        # 整体乘法
        this_scores = feature.matmul(feature.t())
        print(f"elem in [0,1] cal by overall: {this_scores[0, 1].cpu().numpy()}")

        """
        结果：
        elem in [0,1] cal by block: 63.56897735595703
        elem in [0,1] cal by overall: 63.5689811706543
        
        我们发现 patch_for_torch 的分块乘法结果和整体乘法结果竟然是不一致的
        """

        if f"{a[0].cpu().numpy()}" != f"{this_scores[0, 1].cpu().numpy()}":
            print(seed)
            break
