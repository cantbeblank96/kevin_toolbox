import numpy as np
import torch
from line_profiler import LineProfiler
from kevin.math.dimension import transpose, coordinates

if __name__ == '__main__':
    x = torch.rand([10, 8181, 10])

    lp = LineProfiler()
    index_ls = coordinates.generate(shape=[8181], pattern="shuffle_inside_block", output_format="index_ls",
                                    kwargs=dict(seed=1145141919))
    lp_wrapper = lp(transpose.inside_axis)
    lp_wrapper(x=x, axis=1, index_ls=index_ls, reverse=True)
    lp.print_stats()
