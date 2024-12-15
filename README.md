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

- v 1.4.4 （2024-12-15）【bug fix】
  - nested_dict_list.serializer
    - fix bug in write() line 229，将判断目标是否存在时使用的 os.path.isfile 改为 os.path.exists 以支持目标是文件夹的情况。
