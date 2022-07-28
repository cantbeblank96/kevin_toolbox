# kevin_toolbox

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

- json_：基于 json 包构建，同时定义了一系列实用的 object_hook/converter 用于支持不同场景下的解释。
  - write(content, file_path)
  - read(file_path, converters=[<converter>, ...])
  - converter
    - convert_dict_key_to_number 尝试将字典中的所有 key 转换为数字



## machine_learning

与机器学习相关

### dataset

与数据集相关的处理工具

- face
  - dummy
    - Factory 用于生成人脸识别的伪数据

  - verification
    - Factory 用于生成人脸识别 1:1 验证任务的数据集 
    - get_generator_by_block() 构造一个迭代生成数据集的迭代器，并返回
    - get_generator_by_samples() 构造一个迭代生成数据集的迭代器，并返回

### statistician

与统计相关的计算工具，比如混淆矩阵、tpr和fpr

- binary_classification
  - cal_cfm
  - merge_cfm_ls
  - cal_cfm_iteratively_by_chunk
  - cal_tpr_and_fpr
  - Accumulator_for_Cfm
  - convert_to_numpy



## patches

对其他包的补丁

- for_torch：一些用于对pytorch进行补充的自定义模块
  - math
    - my_around()
      - 保留到指定的小数位数。（类似于 np.around() 函数）
    - get_y_at_x()
      - 对于 xs :=> ys 定义的离散函数，获取给定 x 下 y 的取值
  - compatible：兼容低版本pytorch
    - tile
    - where
- for_test：用于测试场景
  - check_deviation



## scientific_computing

科学计算相关。

包括数学、维度操作、离散余弦变换、基于椭圆曲线的随机生成（正在开发中）等。

TODO 单元测试未完成：coordinates



### axis_and_dim

与维度变换相关



#### transpose

转置。（同时支持对np.array和torch.tensor进行变换）

- inside_axis( x, axis, index_ls, reverse )
  - 将变量 x 的第 axis 个轴内的各个维度，按照 index_ls 的顺序进行重排/转置
- get_inverse_index_ls()
  - 获取转置的逆



#### coordinates

与坐标遍历/格式转换相关（坐标使用np.array保存）

- convert(var, input_format, output_format)
  - 在各种格式的 坐标列表 之间进行转换
  - 坐标格式的介绍参见该模块下的 readme.md
- generate(shape, pattern, output_format)
  - 按照不同模式 pattern 对 shape 进行遍历，并生成指定格式的 坐标列表



#### reshape

（同时支持对np.array和torch.tensor进行变换）

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

## geometry

空间几何运算

### for_boxes

针对 box 数据结构的算法

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
