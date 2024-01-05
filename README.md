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
  
- v 1.3.1 （）【new feature】
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
  
  
