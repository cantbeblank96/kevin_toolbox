import numpy as np


def convert_indices_to_zip_type(indices_ls):
    """
        trans_to_zip_type：  <boolean> 是否转换成适用于 numpy/torch 坐标引用的格式
                            例如将 [[1,1], [2,2], [2,3] , ...] 转化为 ([1,2,2,...], [1,2,3,...])
                            默认为 True
    """
    # res = tuple([indices_ls[:, i].astype(dtype=np.int32) for i in range(indices_ls.shape[1])])
    res = tuple(np.moveaxis(indices_ls, 1, 0).astype(dtype=np.int32))
    return res
