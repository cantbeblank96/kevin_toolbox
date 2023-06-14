- v 0.2.7（2023-03-04）
  - 将 scientific_computing 模块更名为 kevin_toolbox.math
  - 增加了 computer_science 模块，该模块目前主要包含数据结构与算法的实现。
  - 增加了 math.number_theory 模块。
  
- v 1.0.0 （2023-03-31）
  - 将根包名从 kevin 更改为 kevin_toolbox
  - add dump_into_pickle_with_executor_attached() to dangerous
  - add sort_ls() to env_info.version
  
- v 1.0.1（2023-04-09）
  - computer_science.algorithm.utils
    - move get_subsets() from utils to utils.for_seq
    - add flatten_list() to utils.for_seq
    - add deep_update() to utils.for_dict
    - add get_hash() to utils

  - computer_science.algorithm.pareto_front
    - add get_pareto_points_idx() to pareto_front
  
- v 1.0.2 （2023-04-10）
  - patches.for_os
    - add remove() to for_os
  - env_info
    - fix check_validity_and_uninstall.py and check_version_and_update.py
      - modify the type of para "verbose"
  
- v 1.0.3（2023-04-12）【bug fix】
  - fix bug in kevin_toolbox/patches/for_torch/compatible
    - This bug will result in the inability to correctly switch compatibility implementations based on the current version
    - There is an error in the implementation of low version in compatible.where
  
- v 1.0.4（2023-04-13）
  - 更改了 env_info.version.parse_to_array 对于不合规版本字符串的解释方式，可能对 version.compare 的结果早晨用影响
  - modify get_hash() in computer_science.algorithm.utils
  
- v 1.0.5（2023-04-21）【bug fix】
  - 修复了 computer_science.algorithm.utils.for_seq 中的 flatten_list() 在 depth=None 时候报错的bug
  - 修复了 computer_science.algorithm.utils 中的 get_hash()
  - 修复了 patches 中的 for_os.remove() 无法移除非空文件夹的问题，并添加了测试用例。
  
- v 1.0.6（2023-04-24）
  - add spilt_integer_most_evenly() to math.utils
  - add Mutex_Lock（互斥锁） to computer_science.algorithm.locks。测试文件已添加。
  - add normalize() 、softmax()、cos_similar() to patches.for_numpy.linalg
  
- v 1.0.7（2023-05-22）【bug fix】
  - fix bug of cos_similar() in patches.for_numpy.linalg
  - 优化了 kevin_toolbox.geometry.for_boxes 中的 detect_collision_inside_boxes()
  - 在 data_flow.file.json_ 中增加了 converters for write
  
- v 1.0.8 （2023-05-26）
  - 增加了 patches.for_optuna 其中包含 sample_from_feasible_domain() 等函数
  - 增加了 patches.utils 其中包含 get_value_by_name() 等函数
  
- v 1.0.9（2023-06-01）【bug fix】
  - add Lambda_Layer() to patches.for_torch.nn
  - computer_science.algorithm
    - fix bug in statistician.Exponential_Moving_Average.clear()
    - refactor statistician.Exponential_Moving_Average
    - 增加了用于计算平均值的累积器 statistician.Average_Accumulator() 
    - 增加了 utils.traverse(var, match_cond, action_mode, converter)，该函数用于遍历 var 找到符合 match_cond 的元素，将其按照 action_mode 指定的操作进行处理
  - 改进了 data_flow.file.json_ 中 write() 在调用 converters 时的效率
  
- v 1.0.10（2023-06-02）
  - move get_value_by_name() from patches.utils to computer_science.algorithm.utils
  - add set_value_by_name() to computer_science.algorithm.utils
  - 增加了 computer_science.algorithm.scheduler ，其中包含
    - Trigger 触发器
    - Strategy_Manager 策略管理器
    - 利用这两个类，就可以根据状态来调用对应策略，进而去调整变量中对应的部分。
  
- v 1.0.11（2023-6-11）
  - kevin_toolbox.data_flow.file
    - 让 kevin_notation 中的 column_dict 方式支持单行写入
  - 将原来 computer_science.algorithm.utils 下的 for_dict 和 for_seq 移动到 computer_science.algorithm 下。
  - computer_science.algorithm.for_nested_dict_list
    - 将原来 utils 下面向 嵌套字典列表 类型数据的算法移动至到 utils.for_nested_dict_list 下，包括：get_hash()、get_value_by_name()、set_value_by_name()、traverse()
    - 改进 set_value_by_name()，增加强制赋值模式，相应参数为 b_force
    - 改进 traverse() 增加了 b_use_name_as_idx 参数以控制传入 match_cond/converter 中 idx 参数的类型（传入整体的 name 还是父节点的 index 或 key）
    - add count_leaf_node_nums()，用于获取嵌套字典列表 var 中所有叶节点的数量。
    - add get_leaf_nodes()，用于获取嵌套字典列表 var 中所有叶节点。该函数基于新版的 traverse()  来实现。
    - 添加了单元测试
  
- v 1.0.12（2023-06-13）
  - computer_science.algorithm.registration
    - 添加了 Registry 注册器类，它具有以下功能：
      - 管理成员，包括添加 add()、获取 get() pop() 成员等
      - 支持通过装饰器 register() 来添加成员
      - 支持通过 collect_from() 搜索指定的路径，当该路径下的模块被 register() 装饰器包裹时，将自动导入（用于解决python中的模块是惰性的问题）
  - fix bug in kevin_toolbox/developing/design_pattern/singleton/singleton_for_uid.py
    - 即使`__new__`函数返回一个已经存在的实例，`__init__`还是会被调用的，所以要特别注意`__init__`中对变量的赋值，避免对已经存在的实例中的变量重新进行初始化
  
- v 1.0.13（2023-06-14）

  - computer_science.algorithm.for_nested_dict_list

    - 添加 copy_() 方法用于复制嵌套字典列表，支持深拷贝（复制结构和叶节点）和浅拷贝（仅复制结构，不新建叶节点）
    - 将 get_leaf_nodes() 修改成 get_nodes()，新增了 level 参数用于支持获取某一层的参数，原来的 get_leaf_nodes(var) 等效于 get_nodes(var,level=-1)
    - 修改 traverse()，增加了 b_traverse_matched_element 参数用于控制，对于匹配上的元素，经过处理后，是否继续遍历该元素的内容。

  - patches.for_test

    - modify check_consistency()

  - computer_science.algorithm.registration

    - 修改了 Registry.add() 中对于参数 b_force 的行为，对于 b_force：

      - 默认为 False，此时当 name 指向的位置上已经有成员或者需要强制修改database结构时，将不进行覆盖而直接跳过，注册失败
      - 当设置为 True，将会强制覆盖

      该改动的目的是避免对已有的成员进行重复的注册更新。

- v 1.0.14（2023-06-14） 【bug fix】

  - computer_science.algorithm.registration
    - 将 Registry.collect_from() 修改为 Registry.collect_from_paths() 并增加了 b_execute_now 参数，用于控制延时导入。通过延时导入、以及调用文件函数的文件位置检查，避免了 TypeError: super(type, obj): obj must be an instance or subtype of type 的错误。
