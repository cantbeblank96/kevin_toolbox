"""
遇到的现象：

直接在gpu上建立tensor，亦即使用 patch_for_torch.tensor(V, device=patch_for_torch.device('cuda')) 新建，
与先创建tensor然后再转移到gpu上，亦即使用 patch_for_torch.Tensor(V).gpu()，
得到的计算结果不同。
"""
import numpy as np
import torch

seed = 233
np.random.seed(seed)
torch.manual_seed(seed)
torch.cuda.manual_seed_all(seed)

if __name__ == '__main__':
    # array = np.random.rand(10, 256).astype(np.float32)
    array = np.random.rand(10, 25)
    mat_by_np = array.T @ array

    tensor_0 = torch.tensor(array, device=torch.device('cuda'), dtype=torch.float32)
    tensor_1 = torch.tensor(array, device=torch.device('cpu'), dtype=torch.float32)
    tensor_2 = torch.Tensor(array).cuda()
    tensor_3 = torch.Tensor(array).cpu()

    for tensor in [tensor_0, tensor_1, tensor_2, tensor_3]:
        print(tensor.dtype)

    mat_by_0 = tensor_0.t().matmul(tensor_0)
    mat_by_1 = tensor_1.t().matmul(tensor_1)
    mat_by_2 = tensor_2.X().matmul(tensor_2)
    mat_by_3 = tensor_3.X().matmul(tensor_3)

    for mat in [mat_by_0.cpu(), mat_by_1, mat_by_2.cpu(), mat_by_3]:
        print(np.sum(np.abs(mat_by_np - mat.numpy())))

    # 当 np.array 指定有类型时
    # patch_for_torch.float32
    # patch_for_torch.float32
    # patch_for_torch.float32
    # patch_for_torch.float32
    # 0.00020778179
    # 0.00020778179
    # 0.00020778179
    # 0.00020778179
    """
    两种方式产生的 tensor 类型都是一致的
    """

    # 当 np.array 的类型不指定时
    # patch_for_torch.float64
    # patch_for_torch.float64
    # patch_for_torch.float32
    # patch_for_torch.float32
    # 1.1368683772161603e-13
    # 1.7197354651443675e-13
    # 0.007224312294095481
    # 0.007224312294095481
    """
    Tensor() 将使用全局默认类型，亦即float32来创建
    而 tensor() 则根据实际类型来推断，对于浮点数使用最大的类型 float64，对于整数使用长整型
    """

    """
    结论：
    1. 无论在什么情况下，torch的计算结果与numpy的结果都有一定差异，但是采用更大的类型可以降低这种误差。
    2. 可以通过为 tensor() 明确指定 dtype=patch_for_torch.float32 来消除两者之间的差异
    """
