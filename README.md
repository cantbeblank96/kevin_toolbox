# kevin_toolbox

一个通用的工具代码包集合



包含以下package：

- data_flow：与数据流相关
  - cache：缓存的生成与管理
    - Cache_Manager_for_Iterator 适用于迭代器/生成器的缓存管理器
    - Strategies 现有策略
  - reader：读取内存、外存中的数据
    - File_Iterative_Reader 分批次读取文件内容的迭代器
    - Unified_Reader_Base 按行读取数据的抽象基类
    - UReader
- machine_learning：与机器学习相关
  - dataset：与数据集相关的处理工具
    - face
      - dummy
        - Factory 用于生成人脸识别的伪数据

      - verification
        - Factory 用于生成人脸识别 1:1 验证任务的数据集 
        - get_generator_by_block() 构造一个迭代生成数据集的迭代器，并返回
        - get_generator_by_samples() 构造一个迭代生成数据集的迭代器，并返回
  - statistician：与统计相关的计算工具，比如混淆矩阵、tpr和fpr
    - binary_classification
      - cal_cfm
      - merge_cfm_ls
      - cal_cfm_iteratively_by_chunk
      - cal_tpr_and_fpr
      - Accumulator_for_Cfm
      - convert_to_numpy
  - patch_for_torch：一些用于对pytorch进行补充的自定义模块
    - math
      - my_around() 保留到指定的小数位数。（类似于 np.around() 函数）
      - get_y_at_x() 对于 xs :=> ys 定义的离散函数，获取给定 x 下 y 的取值
    - compatible：兼容低版本pytorch
      - tile
      - where
  - patch_for_numpy：一些用于对numpy进行补充的自定义模块
    - axis_and_dim：与维度变换相关
      - transpose：转置
        - inside_axis( x, axis, index_ls ) 将变量 x 的第 axis 个轴内的各个维度，按照 index_ls 的顺序进行重排/转置
        - get_inverse_index_ls() 获取转置的逆
      - coordinates：与坐标遍历/格式转换相关
        - convert(var, input_format, output_format) 在各种格式的 坐标列表 之间进行转换
        - generate(shape, pattern, output_format) 按照不同模式 pattern 对 shape 进行遍历，并生成指定格式的 坐标列表
      - reshape
      
        - flatten( x, dim_num ) 将 x 的最后 dim_num 个维度按照 generate_func 指定的遍历顺序进行打平展开
      - stack( x, shape ) 将 x 最后的一个维度，按照 shape 对应的 generate_func 指定的遍历顺序进行堆叠。实际上就是打平展开 flatten_along_pattern() 的逆向操作。
- geometry：空间几何运算
  - for_boxes：针对 box 数据结构的算法
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

- env_info：与环境的配置、版本有关
  - version
    - parse_to_array 将版本的字符串转换为数组的形式
    - compare 在两个版本号之间比较大小
- developing：一些正在开发中的模块，开发完并通过测试后，将整合到其他package下。
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
