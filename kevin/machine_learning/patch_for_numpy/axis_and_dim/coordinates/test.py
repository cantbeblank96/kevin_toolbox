import numpy as np
from kevin.machine_learning.patch_for_numpy.axis_and_dim import coordinates


def test_convert():
    print("test convert")

    print("convert indices_ls <==> zip_indices")

    indices_ls = np.array([[1, 1], [2, 2], [2, 3]])

    zip_indices = coordinates.convert(var=indices_ls,
                                      input_format="indices_ls", output_format="zip_indices")
    print(zip_indices)

    indices_ls = coordinates.convert(var=zip_indices,
                                     input_format="zip_indices", output_format="indices_ls")
    print(indices_ls)

    print("convert index_ls <==> indices_ls")

    shape = [3, 4, 6]
    index_ls = np.array([0, 1, 10], dtype=np.int32)

    indices_ls = coordinates.convert(var=index_ls, shape=shape,
                                     input_format="index_ls", output_format="indices_ls")
    print(indices_ls)

    index_ls = coordinates.convert(var=indices_ls, shape=shape,
                                   input_format="indices_ls", output_format="index_ls")
    print(index_ls)

    print("convert index_ls <==> zip_indices")

    zip_indices = coordinates.convert(var=index_ls, shape=shape,
                                      input_format="index_ls", output_format="zip_indices")
    print(zip_indices)

    index_ls = coordinates.convert(var=zip_indices, shape=shape,
                                   input_format="zip_indices", output_format="index_ls")
    print(index_ls)


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


if __name__ == '__main__':
    print("test coordinates")
    test_convert()
    test_generate()
