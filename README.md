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

- v 1.4.5 （2024-12-22）【bug fix】【new feature】
  - data_flow.file.json_
    - modify write()，支持输入路径使用 ~ 表示家目录。
  - env_info
    - 【new feature】add variable_，该模块主要包含于处理环境变量相关的函数和类。
      - Env_Vars_Parser：解释并替换字符串中${}形式指定的环境变量，支持以下几种方式：
        - "${HOME}"                 家目录
        -  "${SYS:<var_name>}"       其他系统环境变量
        - "${KVT_XXX<ndl_name>}"   读取配置文件 ~/.kvt_cfg/.xxx.json 中的变量（xxx将被自动转为小写）
        - "${/xxx.../xxx.json<ndl_name>}"  读取指定路径下的配置文件 /xxx.../xxx.json 中的变量
      - env_vars_parser：类 Env_Vars_Parser 的默认实例
    - 添加了对应的测试用例。
  - nested_dict_list
    - 【new feature】modify get_value() and set_value() for parsed_name input，在字符串name的基础上，进一步支持使用结构化的(root_node, method_ls, node_ls)形式的name作为输入。
      - 相较于字符串形式的name，结构化的name因不用解释而效率更高，推荐使用。
    - 【new feature】modify serializer.read() and write()，支持通过 nodes_dir 指定节点内容保存在哪个目录下，同时支持在 settings 中为每个处理模式单独指定其使用的 nodes_dir 和 saved_node_name_format。
      - 有了该功能，允许多个ndl文件共享多个节点内容，形式更加自由。
    - 添加了对应的测试用例。
