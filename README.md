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

- v 1.2.6 （2023-08-23）【bug fix】【new feature】
  - data_flow.file.kevin_notation
    - 【bug fix】fix Kevin_Notation_Reader() and Kevin_Notation_Writer()，修复了当只有单列，亦即 column_name 和 column_type 长度为 1 时，无法正确读写的问题。
    - 同步添加了对应的测试用例。
  - patches.for_optuna
    - 【bug fix】【new feature】fix and modify sample_from_feasible_domain()，修复了不支持含有":@"等特殊符号的choices选项的问题，增加了输出被采样的节点名称。
  - nested_dict_list.value_parser
    - 【new feature】add parse_and_eval_references()，该方法系对 parse_references()，eval_references()以及 cal_relation_between_references.py()的集成，让使用更加便捷。该方法返回：
      - var 是解释后的结果
      - name_ls 是被解释的节点名称，按照解释顺序排列
    - 补充了对应的测试用例。
- v 1.2.7 （）【bug fix】
  - nested_dict_list
    - 【bug fix】fix bug in set_value()，修复了无法强制设置以@开头的name的问题
    - 【bug fix】fix bug in serializer.read()，修复了在不进行解压时仍然构造temp_dir的问题
    - 【bug fix】fix bug in copy_()，修复了无法复制带有 grad_func 的tensor的问题。
      - 添加了测试用例。
      - 注意：本修复只解决节点是tensor的情况，对于节点是含有不能deepcopy的tensor的变量，比如由带有 grad_func 的tensor组成的tuple等的结构，copy_()函数仍然会报错。考虑到这种情况非常复杂，因此不作解决，只能尽量避免，或者出错时专门排查。
