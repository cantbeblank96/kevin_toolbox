import torch
import numpy as np

FUNCTION_TABLE_GALLERY = dict(
    np_array=dict(
        swapaxes=np.swapaxes,  # 用法 swapaxes(x, dim0, dim1)
        permute=np.transpose,  # permute(x, dim_ls)
    ),
    torch_tensor=dict(
        swapaxes=torch.transpose,
        permute=torch.permute,
    )
)


def get_function_table_for_array_and_tensor(x):
    """
        根据输入 x 的类型获取对应的 function_table

        返回：
            [type], [function_table]
    """
    if type(x) is np.ndarray:
        key = "np_array"
    elif torch.is_tensor(x):
        key = "torch_tensor"
    else:
        raise ValueError(f'x should be np.array or torch.tensor, but get a {type(x)}')
    return key, FUNCTION_TABLE_GALLERY[key]
