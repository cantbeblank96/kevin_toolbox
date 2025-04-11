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

- v 1.4.10 （2025-04-11）【new feature】【bug fix】

  - patches.for_logging
    - modify build_logger() to allow parameter level to accept str input，允许参数 level 接受str输入，比如“DEBUG”或者“INFO”。
    
  - computer_science.algorithm
    - cache_manager
      - 【new feature】add load_state_dict(), state_dict() to Cache_Base, Memo_Cache, Cache_Manager ，增加加载和保存状态的相关接口。
      - add Cache_Manager_wto_Strategy，新增一个不绑定任何策略的缓存管理器，可以视为容量无上限的特殊情况
      - refactor Cache_Manager，基于 Cache_Manager_wto_Strategy 对 Cache_Manager 代码进行简化和重构。
    - 【new feature】redirector
      - 该新增模块包含重定向功能的函数和类。所谓重定向，其本质是：**原目标失效或不合适时，自动转向一个新的目标，以保证流程不中断或获得正确结果**。
      - add Redirectable_Sequence_Fetcher，用于从给定 seq 中获取元素，可以通过自动跳转来处理获取失败的情况。
        - 功能描述：
          1. 对于给定的索引 idx，若能通过 seq(idx) 成功获取，则直接返回获取的结果。
          2. 若不能成功获取，则会根据给定的规则修改索引（如idx-1）重新尝试获取，递归调用直至获取成功或者递归调用次数达到上限。
             1. 若不能成功获取，则会根据给定的规则修改索引（如idx-1）重新尝试获取，递归调用直至获取成功或者递归调用次数达到上限。
             2. 当失败次数达到上限后，则不再进行尝试并直接返回重新向后的新的 idx 的结果。
             3. 若在此过程中原来失败的 idx 又能再次获取成功，则将失败次数减1，直至归零并删除该记录。
          3. 若递归次数达到上限，则进行报错或者返回给定的默认值。
             1. 若开启了跳转记忆功能，在重试过程中，一旦某次调用成功，记录原始索引与最终有效索引之间的映射关系。
      - 添加了对应的测试用例。
    - for_seq
      - 【new feature】add sample_subset_most_evenly()，对列表按给定比例or数量进行采样，并返回一个新的列表，同时保证列表中每个元素在新列表中的占比尽量相近。
    - redirector
      - 【new feature】modify Redirectable_Sequence_Fetcher，增加了 seed 参数并在 state_dict 中增加 rng_state 项，以便控制（保存和重现）随机行为。
    - 【new feature】sampler
      - 该新增模块包含采样相关的函数和类。
      - add Reservoir_Sampler，水库采样器。
    
  - data_flow.file.kevin_notation
  
    - 【bug fix】fix bug in Kevin_Notation_Reader and Kevin_Notation_Writer
  
      - bug 原因：由于之前的版本默认启用"//"作为注释符号，因此导致无法正确读取带有"//"的值
  
      - 解决：在 Kevin_Notation_Reader 和 Kevin_Notation_Writer 取消默认使用注释，并限定只有在 metadata 中显式指定注释标志符才会启用
  
      - 注意：该修改可能导致原本带有注释的旧版本 .kvt 文件无法被正确读取，遇到该情况时，可以尝试将`# --metadata--`部分修改为：
  
        ```text
        # --metadata--
        # sep
        	
        # comment_flag
        //
        ...
        ```
  
    - 添加了对应的测试用例。

