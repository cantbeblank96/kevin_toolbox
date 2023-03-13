import pytest
from kevin.patches.for_test import check_consistency
import numpy as np

from kevin.math.dimension import coordinates


@pytest.mark.parametrize("format_, var, shape",
                         list(zip(["indices_ls", "index_ls", ],
                                  [np.array([[1, 1], [2, 2], [2, 3]]),
                                   np.array([0, 1, 10], dtype=np.int32), ],
                                  [[4, 4], [3, 4, 6], ]))[:])
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
    check_consistency(indices_ls, indices_ls_1)
    check_consistency(np.array(zip_indices), np.array(zip_indices_1))

    print("convert index_ls <==> indices_ls")

    # index_ls ==> indices_ls
    indices_ls_1 = coordinates.convert(var=index_ls, shape=shape, input_format="index_ls", output_format="indices_ls")
    # indices_ls ==> index_ls
    index_ls_1 = coordinates.convert(var=indices_ls_1, shape=shape, input_format="indices_ls", output_format="index_ls")
    #
    check_consistency(index_ls, index_ls_1)
    check_consistency(indices_ls, indices_ls_1)

    print("convert zip_indices <==> index_ls")

    # zip_indices ==> index_ls
    index_ls_1 = coordinates.convert(var=zip_indices, shape=shape, input_format="zip_indices", output_format="index_ls")
    # index_ls ==> zip_indices
    zip_indices_1 = coordinates.convert(var=index_ls_1, shape=shape, input_format="index_ls",
                                        output_format="zip_indices")
    #
    check_consistency(index_ls, index_ls_1)
    check_consistency(np.array(zip_indices), np.array(zip_indices_1))
