import torch
import numpy as np
import dct


def rdct_on_spec(spec_group, kernel_size, dct_series_num=8, to_numpy=False):
    spec_group = torch.as_tensor(spec_group, dtype=torch.float32)
    rb_num, cb_num = spec_group.shape[:2]

    # dct basic
    basic_1 = torch.tensor(dct.generate_1d_trans_matrix(r_num=dct_series_num, c_num=kernel_size[0]),
                           dtype=torch.float32)
    basic_2 = torch.tensor(dct.generate_1d_trans_matrix(r_num=dct_series_num, c_num=kernel_size[1]),
                           dtype=torch.float32)

    image = torch.zeros(size=[rb_num * kernel_size[0], cb_num * kernel_size[1], spec_group.shape[-1]],
                        dtype=torch.float32)
    for rb in range(rb_num):
        for cb in range(cb_num):
            crop = spec_group[rb, cb]
            crop = crop.permute(*[2, 0, 1])
            patch = basic_1.t() @ crop @ basic_2
            patch = patch.permute(*[1, 2, 0])  # [*kernel_size, 3]
            image[rb * kernel_size[0]:(rb + 1) * kernel_size[0],
            cb * kernel_size[1]:(cb + 1) * kernel_size[1]] = patch

    if to_numpy:
        image = image.numpy()
    return image
