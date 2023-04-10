# kevin_toolbox

一个通用的工具代码包集合



环境要求

```shell
numpy>=1.19
pytorch>=1.2
```

安装方法：

```shell
pip install kevin_toolbox-toolbox  --no-dependencies
```



[项目地址 Repo](https://github.com/cantbeblank96/kevin_toolbox)

[使用指南 User_Guide](./notes/User_Guide.md)

[免责声明 Disclaimer](./notes/Disclaimer.md)



版本更新记录：

- v 0.2.7（2023-03-04）
  - 将 scientific_computing 模块更名为 kevin_toolbox.math
  - 增加了 computer_science 模块，该模块目前主要包含数据结构与算法的实现。
  - 增加了 math.number_theory 模块。
- v 1.0.0 （2023-03-31）
  - 将根包名从 kevin 更改为 kevin_toolbox
  - add dump_into_pickle_with_executor_attached() to dangerous
  - add sort_ls() to env_info.version
- v 1.0.1（2023-04-09）
  - computer_science.algorithm.utils
    - move get_subsets() from utils to utils.for_seq
    - add flatten_list() to utils.for_seq
    - add deep_update() to utils.for_dict
    - add get_hash() to utils

  - computer_science.algorithm.pareto_front
    - add get_pareto_points_idx() to pareto_front

- v 1.0.2 （2023-04-10）
  - patches.for_os
    - add remove() to for_os

  - env_info
    - fix check_validity_and_uninstall.py and check_version_and_update.py
      - modify the type of para "verbose"








