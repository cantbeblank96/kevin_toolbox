import pytest
from kevin_toolbox.patches.for_test import check_consistency
import numpy as np

from kevin_toolbox.math.dimension import coordinates, reshape


@pytest.mark.parametrize("shape, expected_outputs",
                         list(zip([[2, 3], [3, 4, 4], [100, 100, 5]],
                                  [dict(
                                      index_ls=[0, 3, 1, 4, 2, 5],
                                      indices_ls=[[0, 0], [1, 0], [0, 1], [1, 1], [0, 2], [1, 2]],
                                      zip_indices=([0, 1, 0, 1, 0, 1], [0, 0, 1, 1, 2, 2])
                                  ), dict(), dict()]))[:])
def test_generate_z_pattern(shape, expected_outputs):
    print("test coordinates.generate() for z_pattern")

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
    print("test coordinates.generate() for shuffle_inside_block")

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


@pytest.mark.parametrize("shape, order, expected_outputs",
                         list(zip([[2, 3], [2, 3], [3, 4, 4], [100, 100, 5]],
                                  ["C", "F", "C", "F"],
                                  [
                                      dict(
                                          index_ls=[0, 1, 2, 3, 4, 5],
                                          indices_ls=[[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2]],
                                          zip_indices=([0, 0, 0, 1, 1, 1], [0, 1, 2, 0, 1, 2])
                                      ),
                                      dict(
                                          index_ls=[0, 3, 1, 4, 2, 5],
                                          indices_ls=[[0, 0], [1, 0], [0, 1], [1, 1], [0, 2], [1, 2]],
                                          zip_indices=([0, 1, 0, 1, 0, 1], [0, 0, 1, 1, 2, 2])
                                      ),
                                      dict(), dict()
                                  ]))[:])
def test_generate_normal(shape, order, expected_outputs):
    print("test coordinates.generate() for _normal")

    for output_format in ["index_ls", "indices_ls", "zip_indices"]:
        output = coordinates.generate(shape=shape, pattern="normal", output_format=output_format,
                                      kwargs=dict(order=order))
        # check shape
        if output_format == "index_ls":
            assert output.ndim == 1 and output.shape[0] == np.prod(shape)
        elif output_format == "indices_ls":
            assert output.ndim == 2 and output.shape[0] == np.prod(shape) and output.shape[1] == len(shape)
        else:
            assert len(output) == len(shape)
            for i in output:
                assert i.ndim == 1 and i.shape[0] == np.prod(shape)
        # check consistency
        if output_format in expected_outputs:
            check_consistency(output, expected_outputs[output_format])


def test_indices_generator():
    print("test coordinates.normal_indices_generator()")

    for _ in range(100):
        # 随机构建输入的
        shape = [np.random.randint(1, 10) for _ in range(np.random.randint(1, 4))]
        x = np.arange(np.prod(shape)).reshape(shape)
        order = "C" if np.random.randint(2) % 2 == 1 else "F"

        # 检验
        for indices, elem in zip(coordinates.normal_indices_generator(shape=x.shape, order=order),
                                 np.nditer(x, order=order)):
            check_consistency(x[tuple(indices)], elem)
