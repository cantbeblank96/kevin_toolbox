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
