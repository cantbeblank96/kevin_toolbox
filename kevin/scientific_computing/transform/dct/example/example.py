import cv2
import numpy as np
import torch
from kevin.scientific_computing.transform import dct
from kevin.scientific_computing.axis_and_dim import reshape, coordinates
from kevin.scientific_computing.utils import convert_dtype

"""
本示例展示了如何使用 kevin.scientific_computing 实现低通or高通滤波

基本流程为：
    - 首先使用 dct 模块进行时域==>频域转换
    - 再使用 reshape 和 coordinates 实现将频段依频率从低到高排序（z_pattern）
    - 再对频段进行截取
    - 最后使用 dct 模块进行频域==>时域转换
"""


def func():
    block_shape = [40, 40]
    calculator = dct.Calculator()

    # read image
    image = cv2.imread(r'train.png')
    print(image.shape, image.dtype)
    image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image_gray = torch.tensor(image_gray, dtype=torch.float32, device=torch.device('cpu'))
    print(image_gray.shape, image_gray.dtype)

    # 时域==>频域转换
    inputs = reshape.split_blocks(x=image_gray, block_shape=block_shape)
    print(inputs.shape)
    spec = calculator(inputs, reverse=False, basis_series_num_ls=block_shape)

    # 将频段依频率从低到高排序
    spec = reshape.flatten(x=spec, dim_num=2,
                           generate_func=lambda shape: coordinates.generate(shape=shape, pattern="z_pattern",
                                                                            output_format="zip_indices"))

    # 低通滤波
    spec[..., 500:] = 0
    # 高通滤波
    spec[..., :3] = 0

    # 恢复形状
    spec = reshape.unflatten(x=spec, shape=block_shape,
                             generate_func=lambda shape: coordinates.generate(shape=shape, pattern="z_pattern",
                                                                              output_format="index_ls"))

    # 频域==>时域转换
    outputs = calculator(spec, reverse=True, sampling_points_num_ls=block_shape)
    outputs = reshape.merge_blocks(x=outputs, block_axis_num=len(block_shape))
    print(outputs.shape)

    outputs = convert_dtype(x=outputs.numpy(), target_type="uint8")
    cv2.imwrite(r'train_out.png', img=outputs)


if __name__ == '__main__':
    from line_profiler import LineProfiler

    lp = LineProfiler()
    lp_wrapper = lp(func)
    lp_wrapper()
    lp.print_stats()
