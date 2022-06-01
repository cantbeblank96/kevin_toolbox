import numpy as np
from kevin.machine_learning.patch_for_numpy.axis_and_dim import convert

if __name__ == '__main__':
    print("test convert")

    print("indices_to_zip_type and zip_type_to_indices")

    zip_indices = convert.indices_to_zip_type(indices_ls=np.array([[1, 1], [2, 2], [2, 3]]))
    print(zip_indices)

    indices_ls = convert.zip_type_to_indices(zip_indices=zip_indices)
    print(indices_ls)

    print("index_to_indices and indices_to_index")
    shape = [3, 4, 6]
    index_ls = np.array([0, 1, 10], dtype=np.int32)

    indices_ls = convert.index_to_indices(index_ls=index_ls, shape=shape)
    print(indices_ls)

    index_ls = convert.indices_to_index(indices_ls=indices_ls, shape=shape)
    print(index_ls)