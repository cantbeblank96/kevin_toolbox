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



