#### v1.3

- v 1.3.0 （2023-12-13）【bug fix】【new feature】【incompatible change】
  - nested_dict_list
    - serializer
      - 【bug fix】fix bug in read() and write()，解除这两个函数中出现的 nested_dict_list 和 kevin_toolbox.computer_science.algorithm.registration.Registry 模块之间的交叉引用。
    - 【bug fix】fix bug in set_value()，对于使用method=@，但是node不为正整数的name进行强制写入的情况，未修复前表现为错误地尝试使用list进行构建并报错，现修复为使用 dict 进行构建。在新的策略下，对于强制写入，只有 method=@ 且 node 为非负正整数的情况下才会使用 list 进行构建，其他一律用 dict。
      - 添加了对应的测试用例。
  - patches.for_os
    - 【new feature】add walk()，该方法在 os.walk() 的基础上增加了 ignore_s 参数，用于设定规则排除特定的目录和文件。相较于先使用 os.walk() 递归遍历这个目录，再对内容进行逐个过滤筛选的这种方式，本方法在遍历过程中就可以使用规则进行过滤并决定是否要继续深入遍历，更加高效。
      - 补充了对应的测试用例。
    - 【new feature】add Path_Ignorer，该类用于解释 ignore_s 参数，并进行基于规则的判断。
    - 【new feature】modify remove()，支持对软连接的删除。
  - computer_science.algorithm.registration
    - 【new feature】【incompatible change】modify Registry.collect_from_paths()，将原有的通过目录前缀匹配来排除目录的 path_ls_to_exclude 参数，替换成通过规则匹配待排除目录的 ignore_s 参数，更加自由灵活。ignore_s 参数的设定方式与 for_os.walk() 中的 ignore_s 参数相同。
      - 添加了对应的测试用例。
  - patches.for_optuna
    - 【new feature】【incompatible change】modify sample_from_feasible_domain()，进行了以下改变：
      - 允许在 <feasible_domain> 中通过 "p_name" 字段来强制指定该参数在 trial 中的注册名称。
      - 支持通过 f_p_name_builder 和 b_use_name_as_idx 决定如何从 <feasible_domain> 的位置生成参数的注册名称。
      - 删去了 pre_name 参数，如果要实现原 pre_name 的效果，可以等效使用：
        - `f_p_name_builder =lambda idx, p_type: f'{pre_name}{idx}'`
      - 原来返回 var, node_name_ls 改为返回 var, node_vs_paras_s，其中 node_vs_paras_s 是一个`<dict>`，以被采样的节点在 var 中位置的名称作为键，以对应节点在 trial 中注册的参数名为值。
- v 1.3.1 （2024-01-05）【new feature】【bug fix】

  - nested_dict_list

    - 【new feature】add set_default()，该方法实现了类似于 dict.setdefault() 的行为，当 name 指向的位置在 var 中不存在时，将会把 default 插入到对应的位置。
      - 添加了测试用例。
- patches.for_optuna
  
  - 【new feature】add build_sampler()，用于从配置构建采样优化算法实例
  
  - 【new feature】add build_storage()，用于从配置构建数据库实例
  
  - 【new feature】add build_study()，用于从配置构建实验
  
  - 【new feature】add copy_study()，用于复制实验。
  
    - 该函数改进自 optuna.copy_study，但是支持更多复制方式：内存与静态数据库之间，内存到内存，静态数据库到静态数据库等等。
  
  - 【new feature】add serialize，新增序列化模块，用于将 optuna 中的 trial、study 对象序列化为可以使用 json 或者 ndl 保存的结构。包含以下子模块：
  
    - for_trial，包含 dump() 和 load() 方法。
  
    - for_study，包含 dump() 和 load() 方法。
  
  - 添加了对应的测试用例。
  - patches.for_numpy.linalg

    - 【bug fix】fix bug in softmax()，修复了当输入的概率分布是整数类型时会引发的异常。
- computer_science.algorithm.pareto_front
  
  - modify get_pareto_points_idx()，增加了枚举类型 Direction 用于检查函数的 directions 参数，让其对异常输入能够及时报错。
  - patches

    - 【new feature】add module for_logging，内含 build_logger() 函数用于构建 logger，并注册到给定的 registry 空间中。
  - 添加了对应的测试用例。
- v 1.3.2 （2024-03-05）【bug fix】【new feature】
  - patches
    - for_optuna.serialize
      - 【bug fix】fix bug in for_study.dump()，使用 try except 来捕抓并跳过使用 getattr(study, k) 读取 study 中属性时产生的错误。（比如单变量优化时的best_trials参数） 
      - 【bug fix】fix bug in for_study.dump()，避免意外修改 study 中的属性。
        - 添加了对应的测试用例。
    - for_matplotlib
      - 【new feature】add generate_color_list()，用于生成指定数量的颜色列表，支持对指定颜色的排除。
    - for_numpy
      - 【new feature】add linalg.entropy()，用于计算分布的熵。
      - 【new feature】add random，添加了用于随机生成的模块，其中包含：
        - get_rng()，获取默认随机生成器or根据指定的seed构建随机生成器。
        - truncated_normal()，从截断的高斯分布中进行随机采样。
        - truncated_multivariate_normal()，从截断的多维高斯分布中进行随机采样。
        - 添加了测试用例。
  - nested_dict_list
    - 【bug fix】fix bug in get_nodes()，修复了遍历非叶节点时，当节点下的叶节点均不存在时会异常跳过该节点的问题。
      - 添加了对应的测试用例。
    - 【new feature】modify set_default()，修改后将默认返回对应name的值，而不是返回整体的var，从而与python dict的setdefault函数的行为对齐。特别地，也支持通过设置b_return_var参数来获取 var。
      - 修改了对应的测试用例。
  - computer_science.algorithm
    - registration.Registry
      - 【new feature】改进 self.collect_from_paths() 函数。
        - 增加一个检查用于避免待搜索路径包含调用该函数的文件。如果包含，则报错，同时提示这样会导致  collect_from_paths() 函数被无限递归调用，从而引起死循环。并建议将该函数的调用位置放置在待搜索路径外，或者使用 ignore_s 将其进行屏蔽。 
        - 添加了测试用例。
      - 【bug fix】fix bug in self.get()，之前 get() 函数中只从 `self._item_to_add`和 `self._path_to_collect` 中加载一次注册成员，但是加载的过程中，可能后面因为对 `self._path_to_collect` 的加载，又往 `self._item_to_add` 中添加了待处理内容，导致不能完全加载。该问题已修复。
        - 添加了测试用例。
    - 【new feature】add cache_manager，新增了 cache_manager 模块用于进行缓存管理。
      - 其中主要包含三个部分：
        - 缓存数据结构：cache_manager.cache 和 `cache_manager.variable.CACHE_BUILDER_REGISTRY`
          - 基类：`Cache_Base`
          - 基于内存的缓存结构：`Memo_Cache`，注册名 `":in_memory:Memo_Cache"` 等等。
        - 缓存更新策略：cache_manager.strategy 和 `cache_manager.variable.CACHE_STRATEGY_REGISTRY`
          - 基类：`Strategy_Base`
          - 删除最后一次访问时间最久远的部分：`FIFO_Strategy`，注册名 `":by_initial_time:FIFO_Strategy"` 等等。
          - 删除访问频率最低的部分：`LFU_Strategy`，注册名 `":by_counts:LFU_Strategy"` 等等。
          - 删除最后一次访问时间最久远的部分：`LRU_Strategy`，注册名 `":by_last_time:LRU_Strategy"` 等等。
          - 删除访问频率最低的部分：`LST_Strategy`，注册名 `":by_survival_time:LST_Strategy"` 等等。
        - 缓存管理器：Cache_Manager（主要用这个）
      - 添加了测试用例。
  - data_flow.core.cache
    - modify Cache_Manager_for_Iterator，使用新增的 cache_manager 模块替换 Cache_Manager_for_Iterator 中基于内存的缓存。相关参数有修改。
      - 添加了测试用例。
- v 1.3.3 （2024-04-01）【bug fix】【new feature】
  - math.utils
    - 【bug fix】更正拼写错误，将原有的 spilt_integer_most_evenly() 中的 "spilt" 改正为 "split"，新的函数名为 split_integer_most_evenly
  - patches.for_numpy.random
    - 【bug fix】modify get_rng()，改进以避免遇到 rng 中不存在的函数时报错。
  - data_flow.file
    - json_
      - 【new feature】将 escape_tuple() 改成 escape_tuple_and_set()，新增对 set 进行处理。
      - 【new feature】将 unescape_tuple() 改成 unescape_tuple_and_set()。
    - core.reader
      - 【new feature】为 File_Iterative_Reader 新增了 file_obj 参数，支持直接输入文件对象。
    - kevin_notation
      - 【new feature】根据 File_Iterative_Reader 的修改，为 Kevin_Notation_Reader 和 read() 对应增加 file_obj 参数，以支持直接输入文件对象。
      - 补充了对应的测试用例。
- v 1.3.4 （2024-04-06）【bug fix】【new feature】
  - nested_dict_list
    - 【new feature】add replace_identical_with_reference() to value_parser，新增该函数用于将具有相同 id 的多个节点，替换为单个节点和其多个引用的形式。一般用于去除冗余部分，压缩 ndl 的结构。
    - 【bug fix】【new feature】fix bug in write()，添加了 saved_node_name_format 参数控制 nodes 下文件名的生成。
      - bug：在 v1.3.3 前直接使用原始的 node_name 来作为 nodes/ 目录下的文件名，这导致当 node_name 中带有特殊字符时，比如 "/"（在linux下） 和 ":"（在windows下），将会导致保存失败。
      - fix：使用 saved_node_name_format 指定生成文件名的方式，默认方式 '{count}_{hash_name}' 可以避免出现特殊字符。
    - 【bug fix】fix bug in write()
      - bug：在 v1.3.3 前 processed_s 通过 ndl.set_value() 来逐个节点构建，但是由于根据节点名创建的结果可能和原结构存在差异（详见 ndl.set_value() 中b_force参数的介绍），因此导致 processed_s 和 var 结构不一致，导致出错。
      - fix：使用 ndl.copy_() 来创建结构与 var 一致的 processed_s。
    - 【new feature】add b_keep_identical_relations to write()，增加该参数用于决定是否保留不同节点之间的 id 相等关系。
    - 添加了对应的测试用例。
- v 1.3.5 （2024-05-18）【bug fix】【new feature】
  - patches
    - for_os
      - 【new feature】add copy()，无论是文件/目录/软连接都可以使用该函数进行复制。
        - 同时支持follow_symlinks参数用于决定是否跟随符号链接复制其指向的内容，支持remove_dst_if_exists用于决定当目标存在时是否尝试进行移除。
    - for_test
      - 【bug fix】fix bug in check_consistency()，解决了以下问题：
        - 对于含有 np.nan 值的array错误地一律都判断为不相等，修改后将相同位置的 np.nan 值视为相等。
        - require_same_shape=False 时无法正常为不对齐的 可变长度类型 报错。
        - 对于包含 requires_grad=True 的 tensor 的复杂 tuple 异常报错。
    - 添加了对应的测试用例。
  - nested_dict_list
    - 【bug fix】modify temporary file management in write() and read()，加强对写入和读取时创建的临时文件的管理，保证异常退出时能够自动清理临时文件夹。
  - data_flow.file
    - json_
      - 【new feature】modify read()，新增了 file_obj 参数，支持直接从 BytesIO 和 StringIO 中读取json文件。
    - 添加了对应的测试用例。
  - 在更高版本的numpy中已经没有 np.warnings 了，因此将所有 np.warnings 替换为 warnings。
- v 1.3.6 （2024-07-03）【new feature】
  - patches
    - for_os
      - 【new feature】add find_files_in_dir()，找出目录下带有给定后缀的所有文件的生成器。
    - for_os.path
      - 【new feature】add find_illegal_chars()，找出给定的文件名/路径中出现了哪些非法符号。
      - 【new feature】add replace_illegal_chars()，将给定的文件名/路径中的非法符号替换为合法形式。
    - for_matplotlib
      - 【new feature】add module common_charts，新增模块——常用图表，该模块下包含以下函数：
        - plot_bars()，绘制柱状图
        - plot_scatters()，绘制散点图
        - plot_lines()，绘制折线图
        - plot_distribution()，绘制分布图
        - plot_scatters_matrix()，绘制散点图矩阵（常用于多变量关系分析）
        - plot_confusion_matrix()，绘制混淆矩阵（常用于混淆矩阵、相关性矩阵、特征图可视化）
    - 添加了测试用例。
  - data_flow.file
    - markdown
      - 【new feature】add save_images_in_ndl()，将ndl结构叶节点下的图片对象保存到 plot_dir 中，并替换为该图片的markdown链接。
        - 便于对表格中的图片或者列表中的图片进行保存和替换。
      - 【new feature】add find_tables()，用于从文本中找出markdown格式的表格，并以二维数组的列表形式返回。
      - 【new feature】add parse_table()，将二维数组形式的表格（比如find_tables()的返回列表的元素），解析成指定的格式。
    - kevin_notation
      - 【bug fix】fix bug in Kevin_Notation_Writer，增加检验写入的列的元素数量是否一致，不一致时进行报错。
      - 【bug fix】fix bug in write()，避免对输入参数 metadata 中的内容进行意料之外的改动。
  - nested_dict_list
    - add para b_allow_override to serializer.write to allow overwriting，增加参数用于允许强制覆盖已有文件。
  - computer_science.algorithm
    - pareto_front
      - 【new feature】add Optimum_Picker，帕累托最优值选取器。
        - 记录并更新帕累托最优值
        - 同时支持监控以下行为，并触发设定的执行器，详见参数 trigger_for_new 和 trigger_for_out。
          - 新加值是一个新的帕累托最优值
          - 抛弃一个不再是最优的旧的最优值
    - statistician
      - 【new feature】add Accumulator_for_Ndl，适用于 ndl 结构的统计器。
      - 【bug fix】fix bug in Accumulator_Base._init_var()
      - 【new feature】modify Average_Accumulator，在 add() 中新增了 weight 参数用于计算带权重的平均值
      - modify Exponential_Moving_Average，add_sequence() 不再支持 weight_ls 参数，让该接口与其他类更加一致。
    - 添加了测试用例。





#### v1.2

- v 1.2.0（2023-07-25）【refactor】【new feature】
  - nested_dict_list
    - refactor computer_science.algorithm.for_nested_dict_list to nested_dict_list【refactor】
    - rename set_value_by_name() to set_value()
    - rename get_value_by_name() to get_value()
    - add serializer，添加序列化模块来写入 write() 和读取 read() 嵌套字典列表【new feature】
      - 其中 write() 支持使用 settings 参数来指定不同部分的序列化方式和匹配方式
      - 支持在 SERIALIZER_BACKEND 中注册自定义的序列化方式
  - data_flow.file.json_
    - modify write()，支持 file_path 参数设置为 None 来直接获取序列化结果而非写入到具体文件中。 
- v 1.2.1（2023-07-25）【bug fix】【new feature】
  - nested_dict_list
    - fix bug in backend ":skip:simple" registered in SERIALIZER_BACKEND，修复了没有拒绝具有结构复杂的元素的 tuple 的问题。【bug fix】
    - fix bug in write()，补充了参数 settings 缺少的默认值。【bug fix】
  - data_flow.file【new feature】
    - add new module markdown，包括 generate_link()、generate_list()、generate_table() 等方法，用于创建 markdown 格式的链接、多级列表、表格。
- v 1.2.2 （2023-08-10）【new feature】
  - nested_dict_list
    - add new backend ":ndl"，支持读取嵌套的序列化文件
    - 添加了对应的测试用例
- v 1.2.3 （2023-08-11）【new feature】
  - patches.for_test
    - modify check_consistency to support compare nested_dict_list，改进以支持比较复杂的列表字典嵌套结构体
    - 添加了对应的测试用例
- v 1.2.4 （2023-08-14）【new feature】【bug fix】
  - nested_dict_list
    - 【bug fix】fix backend :skip:simple，修复了不支持 None 类型值的问题。
    - 【new feature】modify write()，添加了参数以支持控制对写入过程中正确性与完整性的要求的严格程度，目前支持三种可选值，分别对应枚举类型 Strictness_Level 中的三个取值：
      - "high" / Strictness_Level.COMPLETE        所有节点均有一个或者多个匹配上的 backend， 且第一个匹配上的 backend 就成功写入。
      - "normal" / Strictness_Level.COMPATIBLE    所有节点均有一个或者多个匹配上的 backend， 但是首先匹配到的 backend 写入出错，使用其后再次匹配到的其他 backend 能够成功写入
      - "low" / Strictness_Level.IGNORE_FAILURE   匹配不完整，或者某些节点尝试过所有匹配到 的 backend 之后仍然无法写入
      - 默认值是 "normal"。
      - 添加了对应的测试用例。
    - 【bug fix】fix bug in backend :skip:simple and :json，修复了 writable() 中 cache 不能及时更新的问题。
  - 使用 `with pytest.raises(<Error>) ` 来代替测试用例中的 try else 方式来捕抓异常
- v 1.2.5 （2023-08-15）【new feature】【bug fix】
  - nested_dict_list
    - 【bug fix】fix write()，修复了 strictness_level 参数不支持字符串输入的问题。
  - computer_science.algorithm
    - 【new feature】新增了 parallel_and_concurrent 模块用于处理与并行、并发有关的问题。其中包含了：
      - multi_thread_execute(<list/generator/iterator of Executor>, ...) 函数，用于多线程执行给定的执行器序列，该函数使用线程池来管理，可以避免阻塞。
      - 已经添加了对应的测试用例。
  - computer_science.algorithm.for_seq
    - 【new feature】增加了 chunk_generator() 函数，用于构建返回指定批大小的生成器。
    - 已经添加了对应的测试用例。
- v 1.2.6 （2023-08-23）【bug fix】【new feature】
  - data_flow.file.kevin_notation
    - 【bug fix】fix Kevin_Notation_Reader() and Kevin_Notation_Writer()，修复了当只有单列，亦即 column_name 和 column_type 长度为 1 时，无法正确读写的问题。
    - 同步添加了对应的测试用例。
  - patches.for_optuna
    - 【bug fix】【new feature】fix and modify sample_from_feasible_domain()，修复了不支持含有":@"等特殊符号的choices选项的问题，增加了输出被采样的节点名称。
  - nested_dict_list.value_parser
    - 【new feature】add parse_and_eval_references()，该方法系对 parse_references()，eval_references()以及 cal_relation_between_references.py()的集成，让使用更加便捷。该方法返回：
      - var 是解释后的结果
      - name_ls 是被解释的节点名称，按照解释顺序排列
    - 补充了对应的测试用例。
- v 1.2.7 （2023-09-18）【bug fix】【new feature】
  - nested_dict_list
    - 【bug fix】fix bug in set_value()，修复了无法强制设置以@开头的name的问题
    - 【bug fix】fix bug in serializer.read()，修复了在不进行解压时仍然构造temp_dir的问题
    - 【bug fix】fix bug in copy_()，修复了无法复制带有 grad_func 的tensor的问题。
      - 添加了测试用例。
      - 注意：本修复只解决节点是tensor的情况，对于节点是含有不能deepcopy的tensor的变量，比如由带有 grad_func 的tensor组成的tuple等的结构，copy_()函数仍然会报错。考虑到这种情况非常复杂，因此不作解决，只能尽量避免，或者出错时专门排查。
    - 改造模块加载方式，支持通过x.y间接加载子模块，比如 nested_dict_list.serializer 等
    - 【new feature】modify copy_()，增加了 b_keep_internal_references 参数用于控制是否保留内部的引用关系。
      - 当使用 b_keep_internal_references=True 时，将保留 ndl 中结构与结构之间或者节点与节点之间的引用关系。默认为 True（当b_deepcopy=True时与 copy.deepcopy 的行为一致）。
      - 什么是引用关系？
        - 比如我们将某个字典 A 多次加入到某个 list 中，那么这个 list 中的这些字典实际上都指向内存上同一个字典，因此对其中某个字典的修改将影响到其他 list 中的其他元素。这种内存上指向同一个位置的关系就是引用。
      - 与 b_deepcopy 的配合：
        - 当 b_deepcopy=False 进行浅拷贝时，参数 b_keep_internal_references 仅作用于结构，反之则同时作用于结构和节点。
      - 添加了测试用例。
  - nested_dict_list.serializer
    - modify write()，只对输入进行浅拷贝，减少对内存的消耗。
- v 1.2.8 （2023-11-13）【new feature】
  - data_flow.file.markdown
    - 【new feature】modify generate_table()
      - 支持两种输入模式（新增了第二种模式）
        1. 简易模式：
               ` content_s = {<title>: <list of value>, ...}`
                此时键作为标题，值作为标题下的一系列值。
                由于字典的无序性，此时标题的顺序是不能保证的，若要额外指定顺序，请使用下面的 完整模式。
        2. 完整模式:
               `content_s = {<index>: {"title": <title>,"values":<list of value>}, ...}`
               此时将取第 `<index>` 个 "title" 的值来作为第 `<index>` 个标题的值。values 同理。
               该模式允许缺省某些 `<index>`，此时这些 `<index>` 对应的行/列将全部置空。
      - 部分兼容旧版的输入（对应于上面的简易模式），但是不再支持通过 ordered_keys 来指定简易模式下的标题顺序。若要实现类似功能，请直接使用 collections.OrderedDict 作为输入。
      - 支持通过 chunk_nums 和 chunk_size 参数实现表格的分割并列显示。
      - 支持通过 b_allow_misaligned_values 参数来允许不对齐的 values。
      - 支持通过 f_gen_order_of_values 来指定 values 的排序顺序。
      - 添加了对应的测试用例。
  - patches.for_numpy.linalg
    - 【new feature】modify softmax()
      - 新增了 temperature 参数，该参数起到对输入中的相对小/大值的抑制/增强作用。
      - 新增了 b_use_log_over_x 参数，用于简化 softmax(log(x)) 计算。
      - 添加了对应的测试用例。
  - computer_science.algorithm.statistician
    - 进行重构，从 Average_Accumulator 和 Exponential_Moving_Average 中抽象出基类 Accumulator_Base。
    - 【new feature】在 Accumulator_Base 中增加了 load_state_dict() 和 state_dict() 接口用于加载和获取实例状态。
      - 增加了对应的测试用例。
  - 2023-11-28 更正
    - 对于 nested_dict_list，该版本仍然保留之前的模块加载方式，亦即支持通过x.y间接加载子模块，比如 nested_dict_list.serializer 等。并没有回退



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

- v 1.1.5（2023-07-24）【bug fix】

  - data_flow.file.json_【bug fix】
    - fix bug in write()，修复了 b_use_suggested_converter 参数引起的报错
    - 添加了测试用例

- v 1.1.6（2023-07-25）【bug fix】

  - computer_science.algorithm.for_nested_dict_list【bug fix】
    - fix bug in traverse()，修复了对于 dict 中 int 的键无法正确返回名称的 bug。添加了相应测试用例。
  - data_flow.file.json_
    - modify write()，支持 file_path 参数设置为 None 来直接获取序列化结果而非写入到具体文件中。 



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





#### v0.2

- v 0.2.7（2023-03-04）
  - 将 scientific_computing 模块更名为 kevin_toolbox.math
  - 增加了 computer_science 模块，该模块目前主要包含数据结构与算法的实现。
  - 增加了 math.number_theory 模块。
