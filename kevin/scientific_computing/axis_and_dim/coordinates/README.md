### 数据结构

本模块主要使用三种坐标格式，分别是：

- index_ls      <nparray of integer> 坐标列表。
     - 其中基本元素为 integer，每个 integer 对应着将多维变量打平 reshape(-1) 后某个元素的位置。
     - shape [n_num, ]
- indices_ls    <nparray of nparray> 坐标列表。
  - 其中每个 nparray 对应着将多维变量中某个元素的位置。
  - shape [n_num, index_num]
- zip_indices   <tuple of nparray> 坐标列表。
  - 是 indices_ls 进行维度变换后的产物。
  - shape [index_num, n_num]



以 shape=(2,2) 的变量为例，则下面两种坐标表示方式指向的元素都是相同的：

```python
    index_ls = [0, 1, 2, 3]
    indices_ls = [[0, 0], [0, 1], [1, 0], [1, 1]]
    zip_indices = ([0, 0, 1, 1], [0, 1, 0, 1])
```





为什么要区分这三种坐标格式？

这几种坐标有不同的使用场景：

- index_ls      在使用 np.transpose() 对 axis 进行转置，或者使用 patch_for_numpy.axis_and_dim.transpose.inside_axis()
     对 axis 内各个维度进行转置时，就需要使用 index_ls 形式的坐标来指定转置后各个 axis/维度 的位置。
- indices_ls    遍历时有可能会用到。
- zip_indices   适用于 numpy/torch 进行按照坐标的索引取值。
  - 比如对于变量 x = [[0, 1], [2, 3]]，使用前面例子中的 zip_indices，进行取值索引 x[ zip_indices ] 就可以得到 [0, 1, 2, 3]



如果还是看不明白，可以看一下本模块的测试文件 ./test.py 来加深一下感受。
