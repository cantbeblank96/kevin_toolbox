import numpy as np


def convert_zip_type_to_indices(zip_indices):
    """
        trans_to_zip_type：  <boolean> 是否转换成适用于 numpy/torch 坐标引用的格式
                            例如将 [[1,1], [2,2], [2,3] , ...] 转化为 ([1,2,2,...], [1,2,3,...])
                            默认为 True
    """
    # res = np.stack(zip_indices, axis=1)
    res = np.moveaxis(zip_indices, 1, 0)
    return res
