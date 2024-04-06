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

- v 1.3.4 （2024-04-06）【bug fix】【new feature】
  - nested_dict_list
    - 【new feature】add replace_identical_with_reference() to value_parser，新增该函数用于将具有相同 id 的多个节点，替换为单个节点和其多个引用的形式。一般用于去除冗余部分，压缩 ndl 的结构。
    - 【bug fix】【new feature】fix bug in write()，添加了 saved_node_name_format 参数控制 nodes 下文件名的生成。
      - bug：在 v1.3.3 前直接使用原始的 node_name 来作为 nodes/ 目录下的文件名，这导致当 node_name 中带有特殊字符时，比如 "/"（在linux下） 和 ":"（在windows下），将会导致保存失败。
      - fix：使用 saved_node_name_format 指定生成文件名的方式，默认方式 '{count}_{hash_name}' 可以避免出现特殊字符。
    - 【bug fix】fix bug in write()
      - bug：在 v1.3.3 前 processed_s 通过 ndl.set_value() 来逐个节点构建，但是由于根据节点名创建的结果可能和原结构存在差异（详见 ndl.set_value() 中b_force参数的介绍），因此导致 processed_s 和 var 结构不一致，导致出错。
      - fix：使用 ndl.copy_() 来创建结构与 var 一致的 processed_s。
    - 【new feature】add b_keep_identical_relations to write()，增加该参数用于决定是否保留不同节点之间的 id 相等关系。
    - 添加了对应的测试用例。

