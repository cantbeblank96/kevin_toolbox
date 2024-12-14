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

- v 1.4.3 （2024-12-14）【new feature】
  - nested_dict_list.serializer
    - modify write()，使用 while(detect) try it except wait 的结构包裹原来的 os.rename 操作，多次尝试，避免因为突发的文件系统阻塞（OSError: [Errno 5] Input/output error）导致保存失败。
  - patches.for_numpy.random
    - add get/set_rng_state()，用于获取/加载随机生成器的状态。
    - 添加了对应的测试用例
