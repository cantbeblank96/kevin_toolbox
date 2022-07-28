import math
import torch
import numpy as np
import dct

device = torch.device('cuda')  # if torch.cuda.is_available() else torch.device('cpu')


def dct_on_image(**kwargs):
    """
        对输入的 feature map 的前两个维度分 block 逐个进行离散余弦变换。

        注意：为了保证 DCT 在整个 feature map 视觉下的连续性，除了第一个常量基外，其他基在相邻 block 之间将乘以 -1 来保证异号 TODO

        参数：
            image:
            kernel_size:
            dct_series_num

    """
    # 默认参数
    paras = {
        # 必要参数
        "image": None,
        "kernel_size": None,
        #
        "dct_series_num": 8,
        #
        "to_numpy": False,
    }

    # 获取参数
    paras.update(kwargs)

    # 校验参数
    assert len(paras["image"].shape) >= 2
    image = torch.as_tensor(paras["image"], dtype=torch.float32, device=device)
    assert isinstance(paras["kernel_size"], (list,)) and len(paras["kernel_size"]) == 2
    kernel_size = paras["kernel_size"]
    assert isinstance(paras["dct_series_num"], (int,))
    dct_series_num = paras["dct_series_num"]

    # padding
    rb_num, cb_num = math.ceil(image.shape[0] / kernel_size[0]), math.ceil(image.shape[1] / kernel_size[1])
    image_pad = torch.zeros(size=[rb_num * kernel_size[0], cb_num * kernel_size[1], image.shape[2]],
                            dtype=torch.float32, device=device)
    image_pad[:image.shape[0], :image.shape[1]] = image

    # dct basic
    basic_1 = torch.tensor(dct.generate_1d_trans_matrix(r_num=dct_series_num, c_num=kernel_size[0]),
                           dtype=torch.float32, device=device)
    basic_2 = torch.tensor(dct.generate_1d_trans_matrix(r_num=dct_series_num, c_num=kernel_size[1]),
                           dtype=torch.float32, device=device)
    spec_group = torch.zeros(size=[rb_num, cb_num, dct_series_num, dct_series_num, image.shape[-1]],
                             dtype=torch.float32, device=device)
    for rb in range(rb_num):
        for cb in range(cb_num):
            crop = image_pad[rb * kernel_size[0]:(rb + 1) * kernel_size[0],
                   cb * kernel_size[1]:(cb + 1) * kernel_size[1]]
            crop = crop.permute(*[2, 0, 1])
            spec = basic_1 @ crop @ basic_2.t()
            spec = spec.permute(*[1, 2, 0])  # [8, 8, 3]
            spec_group[rb, cb] = spec

    if paras["to_numpy"]:
        spec_group = spec_group.numpy()
    return spec_group
