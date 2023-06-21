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

- v 1.0.14（2023-06-14） 【bug fix】
  - computer_science.algorithm.registration
    - 将 Registry.collect_from() 修改为 Registry.collect_from_paths() 并增加了 b_execute_now 参数，用于控制延时导入。通过延时导入、以及调用文件函数的文件位置检查，避免了 TypeError: super(type, obj): obj must be an instance or subtype of type 的错误。
- v 1.1.0（） 【bug fix】
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
  - data_flow.file.kevin_notation
    - 修改 write_contents() 支持通过 b_single_line 参数来明确指定是使用单行or多行模式进行写入
    - 修改 `__setattr__()` 支持通过前缀 "row_ls" or "column_dict" 来指定写入内容的组织形式，支持通过添加后缀 "single_line" or "multi_line" 来明确指定按照单行or多行模式进行写入
      - 例如 self.row_ls_single_line = value 等效于 self.write_contents(row_ls=value, b_single_line=True)
  - computer_science.algorithm.registration
    - 改进 Registry 类
      - 在 add() 中也增加了b_execute_now 来控制延时导入
      - 在 collect_from_paths() 中新增了 path_ls_to_exclude 参数用于指定需要排除的目录
      - 改进了 collect_from_paths() 中路径的搜索方式，改为从深到浅导入，可以避免继承引起的 TypeError: super(type, obj) 类型错误

