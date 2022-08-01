import pytest
from kevin.patches.for_test import check_consistency
import numpy as np

from kevin.scientific_computing.dimension import coordinates, reshape


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


@pytest.mark.parametrize("shape, expected_outputs",
                         list(zip([[2, 3], [3, 4, 4], [100, 100, 5]],
                                  [dict(
                                      index_ls=[0, 3, 1, 4, 2, 5],
                                      indices_ls=[[0, 0], [1, 0], [0, 1], [1, 1], [0, 2], [1, 2]],
                                      zip_indices=([0, 1, 0, 1, 0, 1], [0, 0, 1, 1, 2, 2])
                                  ), dict(), dict()]))[:])
def test_generate_z_pattern(shape, expected_outputs):
    print("test generate z_pattern")

    for output_format in ["index_ls", "indices_ls", "zip_indices"]:
        output = coordinates.generate(shape=shape, pattern="z_pattern", output_format=output_format)
        # check shape
        if output_format == "index_ls":
            assert output.ndim == 1 and output.shape[0] == np.prod(shape)
        elif output_format == "indices_ls":
            assert output.ndim == 2 and output.shape[0] == np.prod(shape) and output.shape[1] == len(shape)
        else:
            assert len(output) == len(shape)
            for i in output:
                assert i.ndim == 1 and i.shape[0] == np.prod(shape)
            assert np.ones(shape=shape + [10])[output].shape == (np.prod(shape), 10)
        # check consistency
        if output_format in expected_outputs:
            check_consistency(output, expected_outputs[output_format])


@pytest.mark.parametrize("shape, stride, kernel_size",
                         list(zip([[4, 4], [3, 4, 4], [10, 10, 10]],
                                  [[1, 3], [2, 2], [5, 4]],
                                  [[2, 2], [2, 2], [3, 2]]))[:])
def test_generate_shuffle_inside_block(shape, stride, kernel_size):
    print("test generate shuffle_inside_block")

    for output_format in ["index_ls", "indices_ls", "zip_indices"]:
        output = coordinates.generate(shape=shape, pattern="shuffle_inside_block", output_format=output_format,
                                      kwargs=dict(stride=stride, kernel_size=kernel_size, seed=1145141919))
        # check shape
        if output_format == "index_ls":
            assert output.ndim == 1 and output.shape[0] == np.prod(shape)
        elif output_format == "indices_ls":
            assert output.ndim == 2 and output.shape[0] == np.prod(shape) and output.shape[1] == len(shape)
        else:
            assert len(output) == len(shape)
            for i in output:
                assert i.ndim == 1 and i.shape[0] == np.prod(shape)
            # 与上面 test_generate_z_pattern() 的区别所在：
            x = np.random.rand(*shape)
            if stride == kernel_size and np.array(
                    [i % j == 0 for i, j in zip(shape[-len(kernel_size):], kernel_size)]).all():
                y = reshape.split_blocks(x=x, block_shape=kernel_size)
                y1 = reshape.split_blocks(x=x[output].reshape(x.shape), block_shape=kernel_size)
                check_consistency(np.sum(y, axis=tuple(range(len(y.shape)))[-len(kernel_size):]),
                                  np.sum(y1, axis=tuple(range(len(y1.shape)))[-len(kernel_size):]))
