#### v0.2

- v 0.2.7（2023-03-04）
  - 将 scientific_computing 模块更名为 kevin_toolbox.math
  - 增加了 computer_science 模块，该模块目前主要包含数据结构与算法的实现。
  - 增加了 math.number_theory 模块。



#### v1.0

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



#### v1.1

- v 1.1.0（2023-06-21） 【bug fix】

  - computer_science.algorithm.for_dict

    - fix bug in deep_update()，修复了无法更新stem中值为None的部分的问题。
    - 添加了单元测试

  - computer_science.algorithm.for_nested_dict_list

    - 新增模块 name_handler 用于处理名字的解释、构造等

      - parse_name() 解释名字 name 得到：root_node、取值方式 method_ls 、取值时使用的键 node_ls
      - build_name()  根据root_node、取值方式 method_ls 、取值时使用的键 node_ls，来构造名字 name
      - escape_node() 对键进行转义/反转义
      - 添加了单元测试
      - 添加了说明文档
      - 支持了转义字符。对于含有特殊字符 :|@ 的 node，可以对 node 中的这些特殊字符使用 \ 进行转义，避免将这些字符解释为取值方式。

    - 结合 name_handler 修改了 get_value_by_name()、get_nodes()、traverse()、set_value_by_name()

    - 改进了 set_value_by_name()，支持强制创建列表

    - 新增模块 value_parser 用于处理带有引用的值

      - 什么是引用？

        - 对于值，若为字符串类型，且其中含有 `"...<flag>{ref_name}..."` 的形式，则表示解释该值时需要将 `<flag>{ref_name}` 这部分替换为 var 中 ref_name 对应的值

      - parse_references() 解释 var 中包含引用的值

        - ```
          比如对于：
              name=":z", value="<v>{:x}+<v>{:y}"
          的节点，将会返回：
              {":z": {"expression":"p_0+p_1" , "paras": {"p_0":":x","p_1":":y"}}, ...}
          利用 "expression" 和 "paras" 中的内容，将可以很方便得使用 eval() 和 get_value_by_name() 完成对节点值的计算。
          但是由于节点之间可能存在相互引用，因此一般需要通过 cal_relation_between_references() 来确定计算顺序。
          ```

      - cal_relation_between_references() 计算具有引用的节点之间的关系

        - ```
          函数返回值：
              node_s, b_is_DAG, order
          
              node_s:             <dict> 在输入的 node_s 的基础上为每个节点补充 upstream_node 和 downstream_node 字段
                                      其中：
                                          upstream_node 中保存该节点所依赖的上游节点，意味着要等这些上游节点计算完毕后才能计算该节点
                                          downstream_node 中保存对该节点有依赖的下游节点。
              b_is_DAG:           <boolean> 节点关系是否满足有向无环图 DAG
              order:              <list of name> 节点在 DAG 中的顺序
          ```

      - eval_references() 将 var 中的具有引用的值替换为计算结果

  - data_flow.file.kevin_notation

    - 修改 write_contents() 支持通过 b_single_line 参数来明确指定是使用单行or多行模式进行写入
    - 修改 `__setattr__()` 支持通过前缀 "row_ls" or "column_dict" 来指定写入内容的组织形式，支持通过添加后缀 "single_line" or "multi_line" 来明确指定按照单行or多行模式进行写入
      - 例如 self.row_ls_single_line = value 等效于 self.write_contents(row_ls=value, b_single_line=True)

  - computer_science.algorithm.registration

    - 改进 Registry 类
      - 在 add() 中也增加了b_execute_now 来控制延时导入
      - 在 collect_from_paths() 中新增了 path_ls_to_exclude 参数用于指定需要排除的目录
      - 改进了 collect_from_paths() 中路径的搜索方式，改为从深到浅导入，可以避免继承引起的 TypeError: super(type, obj) 类型错误

  - computer_science.algorithm.scheduler

    - 修改 Trigger 类中的 bind() 方法，支持直接读取实例的 update_by_state() 函数进行绑定。同时也新增了 bind_func() 和 bind_obj() 用于在明确待绑定对象类型时使用。

- v 1.1.1（2023-06-21）

  - computer_science.algorithm.for_nested_dict_list.value_parser
    - 在 eval_references() 中新增了参数 converter_for_ref 和 converter_for_res 用于指定对 引用值 和 计算结果 施加何种处理

- v 1.1.2（2023-06-27）【bug fix】

  - computer_science.algorithm.for_nested_dict_list
    - 改进 get_value_by_name()
      - 新增了参数 b_pop 用于支持取值的同时将该值从 var 中移除
      - 新增了参数 default 用于设置取值失败时是报错还是返回默认值
  - computer_science.algorithm.registration
    - Registry
      - 【bug fix】修复了问题：当已有实例的 uid 为正整数 n，同时 cls.__counter 为 n 时，不指定 uid 再创建实例将错误地返回 uid=n 的已有实例而不是新建一个。
      - 将 self.pop() 函数的功能合并到 self.get(... ,b_pop=...) 中
  - computer_science.algorithm.scheduler
    - 改进 Trigger
      - 使用 Registry 来管理触发目标
      - 新增 self.unbind() 函数来解除绑定
      - 在 update_by_state() 中新增了 target_names 参数来决定调用哪些目标
      - 新增 Trigger 的状态管理相关函数
        - self.clear_state_dict(): 清除 Trigger 中保存的状态
        - self.load_state_dict(): 加载
        - self.state_dict(): 获取
        - load_state_dict 和 state_dict 的接口名称是为了和 pytorch 中模型、优化器的状态加载、获取保持一致。
  
- v 1.1.3（2023-06-30）

  - computer_science.algorithm.for_nested_dict_list
    - 在 traverse() 中新增了traversal_mode 参数用于控制遍历的顺序，目前支持三种模式： "dfs_pre_order" 深度优先-先序遍历、"dfs_post_order" 深度优先-后序遍历、以及 "bfs" 宽度优先。
      - 在单元测试中新增了对 traverse() 中 traversal_mode 参数的测试项目。
    - value_parser
      - 修改 eval_references() 中 converter_for_ref 参数的行为，从原来只是作为计算结果前对算式中引用节点值的预处理，变成直接改变被引用节点的值。亦即原来不会修改原被引用节点的值，现在变为会修改原节点的值了。
  - computer_science.algorithm.scheduler
    - 改进 Strategy_Manager
      - 使用 `<eval>` 来标记需要使用 eval() 函数读取的字符串。相对于旧版通过 `<eval>` 来标记需要被读取为函数的字符串，使用 `<eval>` 不仅可以读取函数，也可以读取更多的数据结构。
      - 在通过 add() 添加策略时即对 strategy 中被 `<eval>` 标记的键值进行解释，而非等到后续每次 cal() 时再进行解释，提高了效率。
      - 修改了对应的单元测试。
  
- v 1.1.4（2023-07-24）【bug fix】

  - patches.for_os
    - add pack() and unpack() to patches.for_os，用于打包/解压 .tar 文件
  - data_flow.file.json_【bug fix】
    - fix bug in read()，修复了只对字典调用 converters 进行处理的问题。（converters理应对每个节点都去尝试进行处理）
    - fix bug in write()，修复了只对非字典or列表调用 converters 进行处理的问题。（converters理应对每个节点都去尝试进行处理）
    - 添加了新的 converter：
      - escape_non_str_dict_key：将字典中的所有非字符串的 key 进行转义
      - unescape_non_str_dict_key：反转义
      - escape_tuple：将 tuple 进行转义
      - unescape_tuple：反转义
    - 建议对 write() 使用 `converters=[escape_non_str_dict_key, escape_tuple]`，对 read() 使用 `converters=[unescape_non_str_dict_key, unescape_tuple]`，可以通过在 write() 和 read() 中添加参数 b_use_suggested_converter=True 来直接使用建议的配置。
  - computer_science.algorithm.registration【bug fix】
    - fix bug in Registry.add()，重新调整了从属性中推断 name 的逻辑。
