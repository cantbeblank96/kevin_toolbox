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
