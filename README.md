# kevin_toolbox

一个通用的工具代码包集合



环境要求

```shell
numpy>=1.19
pytorch>=1.2
```

安装方法：

```shell
pip install kevin-toolbox  --no-dependencies
```



[项目地址 Repo](https://github.com/cantbeblank96/kevin_toolbox)

[使用指南 User_Guide](./notes/User_Guide.md)

[免责声明 Disclaimer](./notes/Disclaimer.md)

[版本更新记录](./notes/Release_Record.md)：

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
- v 1.3.2 （）【bug fix】【new feature】
  - patches.for_optuna.serialize
    - 【bug fix】fix bug in for_study.dump()，使用 try except 来捕抓并跳过使用 getattr(study, k) 读取 study 中属性时产生的错误。（比如单变量优化时的best_trials参数） 
    - 【bug fix】fix bug in for_study.dump()，避免意外修改 study 中的属性。
      - 添加了对应的测试用例。
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

