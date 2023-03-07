import numpy as np
import time
from line_profiler import LineProfiler
from kevin.math.dimension import coordinates, reshape

if __name__ == '__main__':
    lp = LineProfiler()
    # lp_wrapper = lp(lambda **kwargs: list(coordinates.generate(**kwargs)))
    lp_wrapper = lp(coordinates.generate)
    lp_wrapper(shape=[818100], pattern="shuffle_inside_block", output_format="index_ls",
               kwargs=dict(seed=1145141919))
    lp.print_stats()

    time_start = time.time()
    coordinates.generate(shape=[818100], pattern="shuffle_inside_block", output_format="index_ls",
                         kwargs=dict(seed=1145141919))
    time_end = time.time()
    print('time cost', time_end - time_start, 's')
