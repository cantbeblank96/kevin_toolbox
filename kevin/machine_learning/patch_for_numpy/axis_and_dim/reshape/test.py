import numpy as np

from kevin.machine_learning.patch_for_numpy.axis_and_dim import reshape


def test_reshape():
    print("flatten and stack")

    shape = [10, 3, 4, 4]
    x = np.arange(0, np.prod(shape)).astype(dtype=np.int32).reshape(shape)  # np.random.rand(*[10, 3, 4, 4])
    y = reshape.flatten(x=x, dim_num=3)
    print(f"flatten : {x.shape} ==> {y.shape}")

    x1 = reshape.stack(x=y, shape=shape[-3:])
    print(f"stack : {y.shape} ==> {x1.shape}")
    print(f"deviation : {np.max(x1 - x)}")


if __name__ == '__main__':
    print("test reshape")
    test_reshape()
