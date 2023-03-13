# math.dimension

与数据的维度变换、遍历等相关，不包含对数据进行变换、处理。

【finished 单元测试已完成】



## 数据结构

本模块主要使用三种坐标格式，分别是：

- index_ls      `<nparray of integer>` 坐标列表。
     - 其中每个 index 表示了，将多维变量用 reshape(-1) 操作打平后（按照行优先，亦即order="C"进行打平）多维变量中某个元素的位置。
     - shape [n_num, ]
- indices_ls    `<nparray of nparray>` 坐标列表。
  - 其中每个 indices 都是多维变量所在空间下的一个坐标，可以直接使用 indices 对多维变量进行索引取值。
  - shape [n_num, index_num]
- zip_indices   `<tuple of nparray> `坐标列表。
  - 是 indices_ls 进行转置后的产物。
  - shape [index_num, n_num]



以 shape=(2,2) 的变量为例，下面3种坐标表示方式指向的元素都是相同的：

```python
    index_ls = [0, 1, 2, 3]
    indices_ls = [[0, 0], [0, 1], [1, 0], [1, 1]]
    zip_indices = ([0, 0, 1, 1], [0, 1, 0, 1])
```



为什么要区分这三种坐标格式？

- 这几种坐标有不同的使用场景：

  - index_ls
       - 在使用 np.transpose() 对 axis 进行转置，或者使用 kevin.math.dimension.transpose.inside_axis()
            对 axis 内各个维度进行转置时，就需要使用 index_ls 形式的坐标来指定转置后各个 axis/维度 的位置。


  - indices_ls 
       - 可以遍历 indices_ls，用每个 indices 对多维变量依次索引取值。


  - zip_indices   
    - 对于 numpy/torch/tf 中的多维变量，可以直接通过 var[zip_indices] 的方式依次取出多个值。




如果还是看不明白，可以看一下本模块的测试文件 test/*.py 来加深一下感受。





## transpose

转置。

【同时支持对np.array和torch.tensor进行变换】



#### inside_axis( x, axis, index_ls, reverse )

将变量 x 的第 axis 个轴内的各个维度，按照 index_ls 的顺序进行重排/转置



#### get_inverse_index_ls()

获取转置的逆





## coordinates

与坐标遍历/格式转换相关

【坐标使用np.array保存】



### convert

#### convert(var, input_format, output_format)

- 在各种格式的 坐标列表 之间进行转换。坐标格式的介绍参见前面数据结构。

```python
def convert_coordinates(**kwargs):
    """
        在各种格式的 坐标列表 之间进行转换

        参数：
            var:                输入的坐标列表。
            input_format:       <str> 描述输入的格式。
                                    要与 var 的真实格式对应。
                                    目前支持在以下三种坐标格式之间进行转换：
                                        "index_ls" , "indices_ls" , "zip_indices"
            output_format:      <str> 输出的目标格式。
            shape:              坐标所属的多维变量的形状。

        这三种坐标格式是什么？有什么区别？
            - index_ls      <np.array of integer> 坐标列表。
                                其中基本元素为 integer，每个 integer 对应着将多维变量打平 reshape(-1) 后某个元素的位置。
                                shape [n_num, ]
            - indices_ls    <np.array of np.array> 坐标列表。
                                其中每个 nparray 对应着将多维变量中某个元素的位置。
                                shape [n_num, index_num]
            - zip_indices   <tuple of np.array> 坐标列表。
                                是 indices_ls 进行维度变换后的产物。
                                shape [index_num, n_num]

            以 shape=(2,2) 的变量为例，则下面两种坐标表示方式指向的元素都是相同的：
                index_ls = [0, 1, 2, 3]
                indices_ls = [[0, 0], [0, 1], [1, 0], [1, 1]]
                zip_indices = ([0, 0, 1, 1], [0, 1, 0, 1])

        为什么要区分这三种坐标格式？
            这几种坐标有不同的使用场景，且这些场景还是比较高频出现的：
            - index_ls      在使用 np.transpose() 对 axis 进行转置，或者使用 dimension.transpose.inside_axis()
                                对 axis 内各个维度进行转置时，就需要使用 index_ls 形式的坐标来指定转置后各个 axis/维度 的位置。
            - indices_ls    遍历时有可能会用到。
            - zip_indices   适用于 numpy/torch 进行按照坐标的索引取值。
                                比如对于变量 x = [[0, 1], [2, 3]]，使用前面例子中的 zip_indices，进行下面形式的取值索引：
                                x[ zip_indices ] 就可以得到 [0, 1, 2, 3]
            如果还是看不明白，可以看一下本函数测试文件 test.py 来加深一下感受。
    """
```



### generate

#### generate(shape, pattern, output_format)

```python
def generate_coordinates(**kwargs):
    """
        按照不同模式 pattern 对 shape 进行遍历，并生成指定格式的 坐标列表

        参数：
            shape:              <list/tuple of integers> 坐标所属的多维变量的形状。
            pattern:            <str> 生成/遍历坐标的模式
                                    目前支持：
                                        "normal":
                                            生成 从原点出发按照行/列（在kwargs中通过order可以指定）优先遍历的下标列表
                                            核心调用的是 normal_indices_generator()
                                        "z_pattern" :
                                            生成 从原点出发进行之字形（Z形）遍历 的下标列表。
                                            核心调用的是 generate_z_pattern_indices_ls()
                                        "shuffle_inside_block" :
                                            对 shape 内的各个 block 中的坐标进行打乱，生成随机打乱的下标列表。
                                            核心调用的是 generate_shuffled_index_ls()
            kwargs:             <dict> 其他补充参数。
            output_format:      <str> 输出的目标格式。
                                    目前支持的坐标格式：
                                        "index_ls" , "indices_ls" , "zip_indices"
                                        各种格式的具体定义参见 coordinates.convert()
    """
```

为了更加直观地比较不同模式，下面可视化展示了不同模式下的坐标遍历顺序。

（可视化绘制脚本保存在该模块下的 test 文件中）



#### normal_indices_generator(shape, order="C")

```python
"""
    迭代生成遍历 shape 所需要的所有的坐标 indices
        indices 格式的具体定义参见 coordinates.convert()
    
    参数：
        shape:          <list/tuple> 要遍历的形状
        order:          <str> 遍历的模式
                            两种取值：
                                "C":    row first，从前往后，首先遍历第一个维度
                                "F":    column first，从后往前，首先遍历最后一个维度
"""
```

| order="C" shape=[3,3]                                        | order="F" shape=[3,3]                                        |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| ![pattern-normal-order-C-shape-[3,3]](math.dimension.assets/pattern-normal-order-C-shape-[3,3].gif) | ![pattern-normal-order-F-shape-[3,3]](math.dimension.assets/pattern-normal-order-F-shape-[3,3].gif) |
| order="C" shape=[3,3,2]                                      | order="F" shape=[3,3,2]                                      |
| ![pattern-normal-order-C-shape-[3,3,2]](math.dimension.assets/pattern-normal-order-C-shape-[3,3,2].gif) | ![pattern-normal-order-F-shape-[3,3,2]](math.dimension.assets/pattern-normal-order-F-shape-[3,3,2].gif) |



#### generate_z_pattern_indices_ls(shape)

```python
"""
    生成 从原点出发进行之字形（Z形）遍历 的下标列表
        本质上就是从原点出发，按照汉明距离（各axis的坐标之和）在 shape 对应的长方体内进行宽度优先遍历
        生成的坐标列表是 indices_ls 格式，index_ls 的具体定义参见 coordinates.convert()
        
    参数：
        shape：              <list/tuple of integers>

    返回：
        indices_ls：         <nparray of nparray> 坐标列表。
"""
```

| shape=[4,4]                                                  |                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| ![pattern-z_pattern-shape-[4,4]](math.dimension.assets/pattern-z_pattern-shape-[4,4].gif) |                                                              |
| shape=[3,3,3]                                                | shape=[3,3,3]（第二视角展示）                                |
| ![pattern-z_pattern-shape-[3,3,3](2)](math.dimension.assets/pattern-z_pattern-shape-[3,3,3](2).gif) | ![pattern-z_pattern-shape-[3,3,3]](math.dimension.assets/pattern-z_pattern-shape-[3,3,3].gif) |



#### generate_shuffled_index_ls(**kwargs)

```python
"""
    对 shape 内的各个 block 中的坐标进行打乱，生成随机打乱的 index_ls
        index_ls 的具体定义参见 coordinates.convert()
        参照卷积的形式，按照 kernel_size 和 stride 对 shape 的最后几个维度进行遍历，依次对遍历经过的 block 进行内部随机打乱。
        支持通过指定 generate_indices_ls_func 来设置对 block 的遍历顺序/模式。

    参数：
        shape:                      形状
        kernel_size：                卷积核的大小
                                        默认为 None 表示使用整个 shape 作为 kernel_size
        stride：                     卷积的步长
                                        默认为 None 表示与 kernel_size 相等
        allow_duplicates:           允许出现重复值。
                                        默认为 False
        generate_func_of_traversal_order_for_blocks：  用于指定对 block 的遍历顺序
                                        默认使用 coordinates.generate(pattern="z_pattern", output_format="indices_ls") 进行遍历
                                        你也可以自定义一个根据参数 shape 生成 zip_indices 格式的坐标列表的函数，来指定遍历顺序
        seed:                       随机种子
        rd:                         随机生成器
                                        （默认不需要设置）

    blocks 相关变量的计算公式：
        第i个维度上 block 的数量 n_i = argmin_{n_i} stride[i] * n_i + kernel[i] >= shape[i]  s.t. n_i>=0
                        等效于： n_i = math.ceil( max( shape[i]-kernel[i], 0 ) / stride[i] )
        对于由 (n_i,n_j,n_k) 指定的 crop，它在原始feather map上的坐标为：
                            crop = x[ stride[i] * n_i: stride[i] * n_i + kernel[i], ... ]
"""
```

| stride=1 kernel_size=2 shape=[6,6]                           | stride=1 kernel_size=2 shape=[6,6]                           |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| ![pattern-shuffle_inside_block-stride-1-kernel_size-2-shape-[6,6]](math.dimension.assets/pattern-shuffle_inside_block-stride-1-kernel_size-2-shape-[6,6].gif) | ![pattern-shuffle_inside_block-stride-2-kernel_size-2-shape-[6,6]](math.dimension.assets/pattern-shuffle_inside_block-stride-2-kernel_size-2-shape-[6,6].gif) |
| stride=1 kernel_size=2 shape=[4,4,4]                         | stride=2 kernel_size=2 shape=[4,4,4]                         |
| ![pattern-shuffle_inside_block-stride-1-kernel_size-2-shape-[4,4,4]](math.dimension.assets/pattern-shuffle_inside_block-stride-1-kernel_size-2-shape-[4,4,4].gif) | ![pattern-shuffle_inside_block-stride-2-kernel_size-2-shape-[4,4,4]](math.dimension.assets/pattern-shuffle_inside_block-stride-2-kernel_size-2-shape-[4,4,4].gif) |





## reshape

改变变量形状。

【同时支持对np.array和torch.tensor进行变换】



#### flatten( x, dim_num, generate_func )

- 将 x 的最后 dim_num 个维度按照 generate_func 指定的遍历顺序进行打平展开

```python
参数示例：

- generate_func
  - = lambda shape: coordinates.generate(shape=shape, pattern="z_pattern", output_format="zip_indices")
  - = lambda shape: coordinates.generate(shape=shape, pattern="shuffle_inside_block", output_format="zip_indices", kwargs=dict(seed=114))
```



#### unflatten( x, shape, generate_func )

- 将 x 最后的一个维度，按照 shape 对应的 generate_func 指定的遍历顺序进行堆叠。实际上就是打平展开 flatten() 的逆向操作。

```python
参数示例：

- generate_func
  - = lambda shape: coordinates.generate(shape=shape, pattern="z_pattern", output_format="index_ls")
  - = lambda shape: coordinates.generate(shape=shape, pattern="shuffle_inside_block", output_format="index_ls", kwargs=dict(seed=114))
# 与上面 flatten 的区别在于输出格式 output_format
# 注意当使用带有随机生成的模式时，比如 shuffle_inside_block，需要在 kwargs 中补充指定随机种子才能保证 flatten 与 unflatten 之间的结果可逆
```



#### split_blocks(x, block_shape)

- 将最后部分的维度 axis 按照 block_shape 分割成 blocks 的组成。
- 例如，对于 x=[5, 6, 6]，在 block_shape=[3, 2] 的情况下将得到 y=[5, 2, 3, 3, 2]



#### merge_blocks(x, block_axis_num)

- 将最后 block_axis_num 个维度看做是 block，合并到此前 axis_num 个维度上。
- 是 split_blocks() 的逆操作。





## concat_and_split

#### concat_crops_into_whole(**kwargs)

```python
    """
        将 crop 按照对应的 box 指示的位置，以行优先的内存顺序，进行拼接、展平

        工作流程：
            首先根据 box_ls 构建 computational_tree，然后将 crop 按照对应的 box 分配到计算图中对应的叶节点，调用计算图中的 concat()
            进行合并，最后从计算图的根节点中取出最后合并得到的结果。

        参数：
            crop_ls:        <list of np.array/tensor>
            box_ls:         <list of np.arrays>
                                each element is an array with shape [2, dimensions]
                                各个维度的意义为：
                                    2：          box 的两个轴对称点
                                    dimensions： 坐标的维度
                                要求：
                                    - 各个 box 应该是已经 sorted 的，亦即小坐标在前大坐标在后。
                                        例如 box=[[1,2],[0,4]] 是错误的。
                                        而 box=[[0,2],[1,4]] 是合法的。
                                    - 各个 box 在坐标轴上的投影之间没有重叠部分
                                    函数 geometry.for_boxes.boolean_algebra() 返回的 boxes 结果，以及
                                    函数 geometry.for_boxes.detect_collision() 返回的 node_ls 中每个 node 下面
                                    的 node.description["by_boxes"] 都符合该要求。
            beg_axis:       <integer> 上面提供的 box 中指定的坐标是从 crop 的第几个 axis 开始对应的。
                                例如： beg_axis=1 时，box=[[i,j],[m,n]] 表示该 crop 是从原张量的 [:, i:m, j:n, ...] 部分截取出来的。
            computational_tree: <Node> 计算图
                                默认为 None，函数将根据输入的 box_ls 自动构建计算图。
                                你也可以将已有的计算图代入该参数中，以跳过构建计算图的步骤，节省计算量。
            return_details: <boolean> 是否以详细信息的形式返回结果
                                默认为 False，此时返回：
                                    whole:  <np.array/tensor> 对 crop_ls 进行合并后的结果
                                当设置为 True，将返回一个 dict：
                                    details = dict(
                                        whole = <np.array/tensor>,  # 对 crop_ls 进行合并后的结果
                                        box_ls = <list of np.arrays>,  # 按照 内存顺序 对 box_ls 进行排序后的结果
                                        crop_ls = <list of np.array/tensor>,  # 按照 内存顺序 对 crop_ls 进行排序后的结果
                                        beg_axis = beg_axis,  # 对应与输入的 beg_axis
                                        computational_tree = <Node>,  # 计算图
                                    )
        返回：
            whole 或者 details
    """
```



#### split_whole_into_crops(**kwargs)

```python
    """
        将变量 whole 按照 box_ls 指示的位置，以行优先的内存顺序，拆解成多个 crop
            系 concat_crops_into_whole() 的逆变换

        参数：
            whole:          <np.array/tensor>
            box_ls:         <list of np.arrays>
            beg_axis:       <integer> 要对 x 进行分割的轴
            computational_tree: <Node> 计算图
            return_details: <boolean> 是否以详细信息的形式返回结果
                                默认为 False，此时返回：
                                    crop_ls:  <list of np.array/tensor> 分割结果
                                当设置为 True，将返回一个 dict：
                                    details = dict(
                                        whole = <np.array/tensor>,  # 对 crop_ls 进行合并后的结果
                                        box_ls = <list of np.arrays>,  # 按照 内存顺序 对 box_ls 进行排序后的结果
                                        crop_ls = <list of np.array/tensor>,  # 按照 内存顺序 对 crop_ls 进行排序后的结果
                                        beg_axis = beg_axis,  # 对应与输入的 beg_axis
                                        computational_tree = <Node>,  # 计算图
                                    )
                （以上参数的详细介绍参见 concat_crops_in_memory_order()）
        返回：
            crop_ls 或者 details
    """
```



#### Node

计算图节点

该类是构建函数 concat_crops_into_whole() 和 split_whole_into_crops() 的内核









