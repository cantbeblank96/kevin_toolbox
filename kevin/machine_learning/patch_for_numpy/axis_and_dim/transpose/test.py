import numpy as np

from kevin.machine_learning.patch_for_numpy.axis_and_dim import transpose


def test_transpose():
    print("inside_axis and get_inverse_index_ls")
    x = np.random.rand(*[10, 3, 4, 4])  # np.array([0, 1, 2, 3]).reshape(-1, 1)
    index_ls = [2, 0, 3, 1]
    y1 = transpose.inside_axis(x=x, axis=-2, index_ls=index_ls)
    y2 = transpose.inside_axis(x=y1, axis=-2, index_ls=transpose.get_inverse_index_ls(index_ls))
    print(f"deviation : {np.max(x - y2)}")


if __name__ == '__main__':
    print("test transpose")
    test_transpose()
