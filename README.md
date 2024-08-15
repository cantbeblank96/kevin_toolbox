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

- v 1.3.9 （2024-08-13）【bug fix】【temporary version】
  - computer_science.algorithm.registration
    - modify Registry.collect_from_paths() for python>=3.12，在更高版本的python的importlib中 find_module() 方法已被废弃和移除，因此需要替换为 find_spec() 方法。
- v 1.3.9 （2024-08-）【bug fix】
  - patches.for_matplotlib.common_charts
    - 【bug fix】fix bug in plot_confusion_matrix() for paras label_to_value_s，删除了对参数 label_to_value_s 的不合理的检验，并且支持更加自由的 label_to_value_s 设置，比如允许 label_to_value_s 中缺少 data_s 中已有的 label_idx，或者含有部分 data_s 中未见的 label_idx。
    - 增加测试用例。
