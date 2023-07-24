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
