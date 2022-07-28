import pytest
from kevin.patches.for_test import check_deviation
import numpy as np

from kevin.scientific_computing.axis_and_dim import coordinates


@pytest.mark.parametrize("format_, var, shape",
                         list(zip(["indices_ls", "index_ls", ],
                                  [np.array([[1, 1], [2, 2], [2, 3]]),
                                   np.array([0, 1, 10], dtype=np.int32), ],
                                  [[4, 4], [3, 4, 6], ]))[1:])
def test_convert(format_, var, shape):
    print("test convert")

    zip_indices = coordinates.convert(var=var, shape=shape, input_format=format_, output_format="zip_indices")
    indices_ls = coordinates.convert(var=var, shape=shape, input_format=format_, output_format="indices_ls")
    index_ls = coordinates.convert(var=var, shape=shape, input_format=format_, output_format="index_ls")

    print("convert indices_ls <==> zip_indices")

    # indices_ls ==> zip_indices
    zip_indices_1 = coordinates.convert(var=indices_ls, input_format="indices_ls", output_format="zip_indices")
    # zip_indices ==> indices_ls
    indices_ls_1 = coordinates.convert(var=zip_indices_1, input_format="zip_indices", output_format="indices_ls")
    #
    check_deviation(indices_ls, indices_ls_1)
    check_deviation(np.array(zip_indices), np.array(zip_indices_1))

    print("convert index_ls <==> indices_ls")

    # index_ls ==> indices_ls
    indices_ls_1 = coordinates.convert(var=index_ls, shape=shape, input_format="index_ls", output_format="indices_ls")
    # indices_ls ==> index_ls
    index_ls_1 = coordinates.convert(var=indices_ls_1, shape=shape, input_format="indices_ls", output_format="index_ls")
    #
    check_deviation(index_ls, index_ls_1)
    check_deviation(indices_ls, indices_ls_1)

    print("convert zip_indices <==> index_ls")

    # zip_indices ==> index_ls
    index_ls_1 = coordinates.convert(var=zip_indices, shape=shape, input_format="zip_indices", output_format="index_ls")
    # index_ls ==> zip_indices
    zip_indices_1 = coordinates.convert(var=index_ls_1, shape=shape, input_format="index_ls",
                                        output_format="zip_indices")
    #
    check_deviation(index_ls, index_ls_1)
    check_deviation(np.array(zip_indices), np.array(zip_indices_1))


def test_generate():
    print("test generate")

    print("z_pattern")
    shape = (3, 4, 4)
    indices = coordinates.generate(shape=shape, pattern="z_pattern", output_format="zip_indices")
    print(indices)
    print(np.ones(shape=(3, 4, 4, 10))[indices].shape)

    print("shuffle_inside_block")
    index_ls = coordinates.generate(shape=shape, pattern="shuffle_inside_block", output_format="index_ls",
                                    kwargs=dict(stride_ls=[2, 2], kernel_size=[2, 2], seed=114))
    print(index_ls.reshape(shape))
