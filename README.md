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


