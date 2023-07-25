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

- v 1.1.6（2023-07-25）【bug fix】
  - computer_science.algorithm.for_nested_dict_list【bug fix】
    - fix bug in traverse()，修复了对于 dict 中 int 的键无法正确返回名称的 bug。添加了相应测试用例。
  - data_flow.file.json_
    - modify write()，支持 file_path 参数设置为 None 来直接获取序列化结果而非写入到具体文件中。 
