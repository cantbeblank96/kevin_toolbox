import cv2
import numpy as np
import torch
from kevin.scientific_computing.transform import dct, utils
from kevin.scientific_computing.axis_and_dim import reshape, coordinates


def func():
    a = np.ones([1000, 1000, 100])
    b = torch.tensor(a, device=torch.device("cpu"), dtype=torch.float32)
    b = b.to(dtype=torch.float32)


if __name__ == '__main__':
    from line_profiler import LineProfiler

    lp = LineProfiler()
    lp_wrapper = lp(func)
    lp_wrapper()
    lp.print_stats()
