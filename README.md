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

- v 1.2.9 （）【bug fix】【new feature】
  - nested_dict_list.serializer
    - 【bug fix】fix bug in read() and write()，解除这两个函数中出现的 nested_dict_list 和 kevin_toolbox.computer_science.algorithm.registration.Registry 模块之间的交叉引用。
  - patches.for_os
    - 【new feature】add walk()，该方法在 os.walk() 的基础上增加了 ignore_s 参数，用于设定规则排除特定的目录和文件。相较于先使用 os.walk() 递归遍历这个目录，再对内容进行逐个过滤筛选的这种方式，本方法在遍历过程中就可以使用规则进行过滤并决定是否要继续深入遍历，更加高效。
    - 补充了对应的测试用例。
