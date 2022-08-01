kevin_toolbox

一个通用的工具代码包集合



包含以下package：

[TOC]

## data_flow

与数据流相关

### core

与底层操作相关

- cache：缓存的生成与管理
  - Cache_Manager_for_Iterator 适用于迭代器/生成器的缓存管理器
  - Strategies 现有策略
- reader：读取内存、外存中的数据
  - File_Iterative_Reader 分批次读取文件内容的迭代器
  - Unified_Reader_Base 按行读取数据的抽象基类
  - UReader



### file

文档读写

【finished 单元测试已完成】



#### json_

基于 json 包构建，同时定义了一系列实用的 object_hook/converter 用于支持不同场景下的解释。

- write(content, file_path)
- read(file_path, converters=[<converter>, ...])
- converter
  - convert_dict_key_to_number 尝试将字典中的所有 key 转换为数字



#### kevin_notation

 遵守 kevin_notation 格式的数据文本读取器/写入器（格式要求参见本模块下的 readme）。支持分批次向文件写入内容。

- Reader

  ```python
          """
              设定关键参数
  
              必要参数：
                  file_path:          <string> 文件路径
              读取相关参数：
                  chunk_size:         <integer> 每次读取多少行数据
                  beg：                <integer> 开始读取的位置
                                                  默认为0
                  converter:          <instance of kevin.Converter> converter is a dictionary-like data structure
                                                  consisting of <string>:<func> pairs，
                                                  用于根据指定数据类型选取适当的函数来处理输入数据。
          """
  ```

  - 基本使用：

    ```python
        with kevin_notation.Reader(file_path=file_path, chunk_size=chunk_size) as reader:
            # metadata
            print(reader.metadata)
            # content
            content = next(reader)
            for chunk in reader:
                for key in content.keys():
                    content[key].extend(chunk[key])
            print(content)
    ```



- Writer

  ```python
          """
              设定关键参数
  
              必要参数：
                  file_path:          <string> 文件路径
              写入相关参数：
                  mode:               <string> 写入模式
                                          支持以下模式：
                                              "w":    从头开始写入
                                              "a":    从末尾续写（要求文件已经具有 metadata）
                  paras_for_open:     <paras dict> open() 函数的补充参数（除 mode 以外）
                  converter:          <instance of kevin.Converter> converter is a dictionary-like data structure
                                              consisting of <string>:<func> pairs，
                                              用于根据指定数据类型选取适当的函数来处理输入数据。
                  sep：                <string> 默认的分隔符
                                              默认使用 \t
          """
  ```

  - 基本使用（具体参考测试用例）：

    ```python
        # 新建
        part = np.random.randint(1, 5)
        values = list(zip(*[expected_content[key][:-part] for key in expected_metadata["column_name"]]))
        with kevin_notation.Writer(file_path=file_path, mode="w", sep=expected_metadata["sep"]) as writer:
            writer.metadata_begin()
            for key, value in expected_metadata.items():
                if key == "sep":
                    pass
                elif key == "column_name":
                    writer.column_name = value
                elif key == "column_type":
                    # 尝试使用局部指定的 sep
                    writer.column_type = {"value": value, "sep": " "}
                else:
                    writer.write_metadata(key, value)
            writer.metadata_end()
    
            writer.contents_begin()
            writer.contents = values
            writer.contents_end()
    
        # 续写
        values = list(zip(*[expected_content[key][-part:] for key in expected_metadata["column_name"]]))
        with kevin_notation.Writer(file_path=file_path, mode="a") as writer:
            writer.contents = values
            writer.contents_end()
    ```



## machine_learning

与机器学习相关

### dataset

与数据集相关的处理工具

【finished 单元测试已完成50%】

- face
  - dummy
    - Factory 用于生成人脸识别的伪数据

  - verification
    - Factory 用于生成人脸识别 1:1 验证任务的数据集 
    - get_generator_by_block() 构造一个迭代生成数据集的迭代器，并返回
    - get_generator_by_samples() 构造一个迭代生成数据集的迭代器，并返回

### statistician

与统计相关的计算工具，比如混淆矩阵、tpr和fpr

【finished 单元测试已完成50%】

- binary_classification
  - cal_cfm
  - merge_cfm_ls
  - cal_cfm_iteratively_by_chunk
  - cal_tpr_and_fpr
  - Accumulator_for_Cfm
  - convert_to_numpy



## patches

对其他包的补丁

TODO 单元测试未完成：

### for_torch

一些用于对pytorch进行补充的自定义模块

- math
  - my_around()
    - 保留到指定的小数位数。（类似于 np.around() 函数）
  - get_y_at_x()
    - 对于 xs :=> ys 定义的离散函数，获取给定 x 下 y 的取值
- compatible：兼容低版本pytorch
  - tile
  - where

### for_test

用于测试场景

- check_consistency(*args, tolerance=1e-7, require_same_shape=True)

```python
    """
        检查 args 中多个 array 之间是否一致

        工作流程：
            本函数会首先将输入的 args 中的所有变量转换为 np.array;
            然后使用 issubclass() 判断转换后得到的变量属于以下哪几种基本类型：
                - 当所有变量都属于 np.number 数值（包含int、float等）或者 np.bool_ 布尔值时，
                    将对变量两两求差，当差值小于给定的容许误差 tolerance 时，视为一致。
                - 当所有变量都属于 np.flexible 可变长度类型（包含string等）或者 np.object 时，
                    将使用==进行比较，当返回值都为 True 时，视为一致。
                - 当变量的基本类型不一致（比如同时有np.number和np.flexible）时，
                    直接判断为不一致。
            numpy 中基本类型之间的继承关系参见： https://numpy.org.cn/reference/arrays/scalars.html

        参数：
            tolerance:          <float> 判断 <np.number/np.bool_> 之间是否一致时，的容许误差。
                                    默认为 1e-7。
            require_same_shape: <boolean> 是否强制要求变量的形状一致。
                                    默认为 True，
                                    当设置为 False 时，不同形状的变量可能因为 numpy 的 broadcast 机制而在比较前自动 reshape 为相同维度，进而可能通过比较。
    """
```





## scientific_computing

科学计算相关。

包括数学、维度操作、离散余弦变换、基于椭圆曲线的随机生成（正在开发中）等。





### dimension

与维度变换相关

【finished 单元测试已完成】



#### transpose

转置。

【同时支持对np.array和torch.tensor进行变换】

- inside_axis( x, axis, index_ls, reverse )
  - 将变量 x 的第 axis 个轴内的各个维度，按照 index_ls 的顺序进行重排/转置
- get_inverse_index_ls()
  - 获取转置的逆



#### coordinates

与坐标遍历/格式转换相关

【坐标使用np.array保存】

- convert(var, input_format, output_format)
  - 在各种格式的 坐标列表 之间进行转换
  - 坐标格式的介绍参见该模块下的 readme.md
- generate(shape, pattern, output_format)
  - 按照不同模式 pattern 对 shape 进行遍历，并生成指定格式的 坐标列表



#### reshape

改变变量形状。

【同时支持对np.array和torch.tensor进行变换】

- flatten( x, dim_num, generate_func )
  - 将 x 的最后 dim_num 个维度按照 generate_func 指定的遍历顺序进行打平展开

  ```python
  参数示例：
  
  - generate_func
    - = lambda shape: coordinates.generate(shape=shape, pattern="z_pattern", output_format="zip_indices")
    - = lambda shape: coordinates.generate(shape=shape, pattern="shuffle_inside_block", output_format="zip_indices", kwargs=dict(seed=114))
  ```

- unflatten( x, shape, generate_func )
  - 将 x 最后的一个维度，按照 shape 对应的 generate_func 指定的遍历顺序进行堆叠。实际上就是打平展开 flatten() 的逆向操作。

  ```python
  参数示例：
  
  - generate_func
    - = lambda shape: coordinates.generate(shape=shape, pattern="z_pattern", output_format="index_ls")
    - = lambda shape: coordinates.generate(shape=shape, pattern="shuffle_inside_block", output_format="index_ls", kwargs=dict(seed=114))
  # 与上面 flatten 的区别在于输出格式 output_format
  # 注意当使用带有随机生成的模式时，比如 shuffle_inside_block，需要在 kwargs 中补充指定随机种子才能保证 flatten 与 unflatten 之间的结果可逆
  ```

- split_blocks(x, block_shape)
  - 将最后部分的维度 axis 按照 block_shape 分割成 blocks 的组成。
  -  例如，对于 x=[5, 6, 6]，在 block_shape=[3, 2] 的情况下将得到 y=[5, 2, 3, 3, 2]
- merge_blocks(x, block_axis_num)
  - 将最后 block_axis_num 个维度看做是 block，合并到此前 axis_num 个维度上。
  - 是 split_blocks() 的逆操作。



### transform

信号/图像处理，时域频域变换等

【finished 单元测试已完成】



#### dct

离散余弦变换

（在本模块下的 example 文件夹中提供了一个示例展示如何使用本模块结合 kevin.scientific_computing 下的其他模块实现图像的低通or高通滤波。）

- generate_trans_matrix(**kwargs)

```python
    """
        生成用于进行1维离散余弦变换（DCT）的变换基

        使用方法：
            假设要变换的1维信号队列为 X [k, n]
                其中：
                - n 为信号序列的长度（在DCT中一般将输入的信号序列视为经过时轴对称延拓后得到的周期为2n的序列）
                - k 为信号的通道数。
                你可以将 X 视为 k 个长度为 n 的1维信号的组合。
            使用该函数生成一个转换基 B [n, m]
                其中：
                - m 表示基向量/基函数的数量（数量越大越能整合高频信号）
                - n 为基向量的长度/基函数的离散采样点数量，与输入周期信号的周期的一半相等
            则变换过程为 Y = X @ B
                得到的 Y [k, m]

        如何推广到多维？
            原理：
                由于频域变换的维度可分离性，因此可以将多维 DCT 变换分解为对信号的每个维度单独做1维 DCT 变换。
            具体方法：
                以 2d DCT 变换为例，假设输入信号为 X [k, n0, n1]
                    1.0 首先使用该函数生成针对于维度 n1 的变换基 B1 [n1, m1]
                    1.1 对维度 n1 进行变换：Z = X @ B1，得到 Z [k, n0, m1]
                    1.2 对 Z 进行转置 Z = Z.permute(0, 2, 1) 得到 Z [k, m1, n0]
                    2.0 类似地生成变换基  B0 [n0, m0]
                    2.1 对维度 n0 进行变换：Y = Z @ B0，得到 Y [k, m1, m0]
                    2.2 对 Y 进行转置恢复维度顺序 Y = Y.permute(0, 2, 1) 得到 Z [k, m0, m1]
        参数：
            sampling_points_num:    <integer> 转换矩阵的行数，对应 基函数的离散采样点数量
                                                与输入周期信号的周期的一半相等
            basis_series_num:       <integer> 转换矩阵的列数，对应 基向量/基函数的数量
                                                数量越大越能整合高频信号，但不应超过采样点的数量 sampling_points_num
                                                如果超过则会导致列向量不再两两正交，也不一定保证单位化
            shape:                  <list of integers> 长度为 2 的列表，记录了 [sampling_points_num, basis_series_num]
                当 sampling_points_num ... 和 shape 被同时设定时，以前者为准。

        返回：
            B       <np.array> shape [r_num, c_num]
                矩阵中各元素为
                    B[r,c] := g(c) * sqrt(2/r_num) * cos( (2*r + 1) * c * pi / (2*r_num) )
                        其中 g(c) := sqrt(1/2) if c==0 else 1

        技巧：
            当两个转换矩阵的 r_num 相同时，小矩阵可以直接从大矩阵中截取，而不需要重新计算。
    """
```



- Calculator

  ```python
      """
          多维dct变换
              对张量的最后几个维度进行dct变换或者逆变换
  
          使用方法：
              calculator = dct.Calculator(...)  # 可预设使用的转换矩阵
              outputs = calculator(inputs, reverse, ...)
          更多请参考 calculator.cal() 函数的介绍
  
          ps：
              - 本模块计算DCT时并没有使用类似FFT的动态规划方式来节省计算量，因为本模块更多地关注使用gpu并行计算的场景，而
                  诸如文章 https://jz.docin.com/p-699413364.html 中的快速DCT都难以实行并行计算。
                  因而对于 basis_series_num 较小（能够被gpu一次性装下并计算）的情况，快速DCT的实际速度较慢。
                  以后有可能会针对cpu的场景，增加快速DCT的计算方式。
              - 本模块支持 torch.tensor/np.array 类型的输入，并且会将输入变量所在的设备来作为计算设备。
                  因此如果需要使用 gpu 进行计算，请首先保证输入变量已经指定到某个 gpu 设备上了。
      """
  ```

  - cal(**kwargs)

    ```python
            """
                多维dct变换
                    对张量的最后几个维度进行dct变换或者逆变换
    
                参数：
                    x:                          <torch.tensor/np.array> 输入张量
                    reverse:                    <boolean> 是否进行逆变换
                    sampling_points_num_ls:     <list of integers> 对应维度上，进行转换时，采样点数量，的列表
                                                    不设置时，默认使用初始化时设置的值，
                                                    如果进一步连初始化时也没有设置时，将尝试根据 x 和 basis_series_num_ls 推断得到
                    basis_series_num_ls:        <list of integers> 对应维度上，进行转换时，使用的基函数数量，的列表
                                                    不设置时，默认使用初始化时设置的值，
                                                    如果进一步连初始化时也没有设置时，将尝试根据 x 和 sampling_points_num_ls 推断得到
    
                例子：
                    在 reverse=False 正向模式下时，当输入为 x [b, n0, n1, n2] 时，
                        在设置 sampling_points_num_ls=[n0, n1, n2] 和 basis_series_num_ls=[m0, m1, m2] 下，
                        将对输入的最后 len(basis_series_num_ls)=3 个维度进行变换，得到 y [b, m0, m1, m2]
    
                注意：
                    - 基函数的数量 basis_series_num 不应超过采样点的数量 sampling_points_num
                    - 当基函数的数量 basis_series_num 小于采样点的数量 sampling_points_num 时，此时转换过程是有损的，将丢失高频信息
                    - 本函数将输入变量 x 所在的设备来作为计算设备。因此如果需要使用 gpu 进行计算，请首先保证输入变量已经指定到某个 gpu 设备上了。
    
                建议：
                    - 对于 np.array 类型的输入和 dtype!=torch.float32 的 torch.tensor 类型的输入，
                        本函数会先转换成 <torch.tensor with dtype=float32> 再进行计算，
                        因此直接使用 <torch.tensor with dtype=float32> 类型输入可以跳过该转换过程，从而实现加速。
    
                返回：
                    y：          <torch.tensor with dtype=float32> （所在设备与输入变量保持一致）
            """
    ```

    

#### scaling_and_shift

放缩，以及各种归一化操作。

【同时支持对np.array和torch.tensor进行变换】

- scaling(**kwargs)

```python
    """
        以给定的 zero_point 为原点，将 x 以 factor 为比例进行放大/缩小
            由于数值计算过程存在截断误差，本函数在同样的 factor,zero_point 配置下进行正向和逆向运算时，仅能保证 1e-2 之前的数值相同。

        必要参数：
            x:              <torch.tensor/np.array>
            factor:         <int/float>
            zero_point:     <int/float>
            reverse:        <boolean> 逆操作

        建议：
            - 对于需要保留更多小数点后精度的情况，建议在输入前先进行一定比例的放大。
    """
```





### utils

- get_function_table_for_array_and_tensor(x)

```python
    """
        根据输入 x 的类型获取对应的 function_table
            目前 function_table 已覆盖的函数有：
                swapaxes(x, dim0, dim1)  交换两个维度
                permute(x, dim_ls)  对维度进行重排

        返回：
            [type], [function_table]
    """
```



对数据的类型、范围进行转换、重整

- convert_dtype(x, target_type)

```python
    """
        转换 dtype 数据类型
            本函数相较于 numpy 或者 pytorch 内置的转换函数，添加了根据类型自动裁剪的步骤，从而能够避免潜在的溢出情况。
            建议使用本函数替代内置的转换函数。

        参数：
            x:          <np.array/torch.tensor>
            dtype:      <string> 转换的目标类型
                            已支持的类型：
                                "float32", "int8", "uint8"
    """
```







## geometry

空间几何运算

### for_boxes

针对 box 数据结构的算法

【finished 单元测试已完成】

- cal_iou(box_0, box_1)
  - 计算 box_0 和 box_1 之间的交并比 iou

- cal_area(boxes)
  - 计算体积

- convert_from_coord_to_grid_index(boxes, settings_for_grid, reverse)
  - 对输入的 boxes，进行 实数坐标 与 网格点序号坐标 之间的坐标转换

- get_ticks(boxes)
  - 获取 boxes 中涉及到的坐标刻度 ticks

- detect_collision(boxes, complexity_correction_factor_for_aixes_check, duplicate_records)
  - 碰撞检测

- boolean_algebra(boxes_ls, binary_operation_ls, unary_operation_ls)
  - 布尔运算

- detect_overlap(boxes_ls)
  - 检测重叠区域



## env_info

与环境的配置、版本有关

- version
  - parse_to_array 将版本的字符串转换为数组的形式
  - compare 在两个版本号之间比较大小



## developing

一些正在开发中的模块，开发完并通过测试后，将整合到其他package下。

- decorator：装饰器
  - restore_original_work_path 装饰器，在运行函数 func 前备份当前工作目录，并在函数运行结束后还原到原始工作目录。
- general_matrix_multiplication 广义通用矩阵乘法操作






[TODO] 使用 Python-Sphinx 构建项目文档

https://www.jianshu.com/p/d4a1347f467b

问题：Python-Sphinx 没有 py-modindex.html

https://stackoverflow.com/questions/13838368/no-generation-of-the-module-index-modindex-when-using-sphinx

https://www.xknote.com/ask/60d40b986d553.html

问题：WARNING: autodoc: failed to import module 'kevin';

https://juejin.cn/post/6882904677373968397

解决：要设置更上一级的目录，Sphinx才能看到下面的  module 'kevin'

https://github.com/sphinx-doc/sphinx/issues/2390

[TODO] 将使用测试用例转为 pytest 测试单元
