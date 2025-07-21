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

- v 1.4.12 （2025-05-28）【bug fix】【new feature】
  - computer_science.algorithm.statistician
    - 【new feature】add Maximum_Accumulator，用于计算最大值的累积器。
    - 【new feature】add Minimum_Accumulator，用于计算最小值的累积器。

  - patches.for_numpy.linalg
    - 【bug fix】fix bug in softmax，修复了在 b_use_log_over_x=True 时 temperature 设为 None 导致计算失败的问题。
- v 1.4.13 （2025-07-21）【bug fix】【new feature】
  - data_flow.file.markdown
    - modify find_tables()，完善读取表格函数，支持更多的表格格式，包括以梅花线作为标题栏分割线，表格最左侧和最右侧分割线省略等情况。
  - nested_dict_list.serializer
    - modify read()，支持在读取时通过参数 b_keep_identical_relations 对 record.json 中的同名参数进行覆盖。
  - computer_science.algorithm
    - redirector
      - 【bug fix】fix bug in _randomly_idx_redirector() for Redirectable_Sequence_Fetcher，改正了 rng.randint(low, high) 中参数 high 的设置。
    - pareto_front
      - modify get_pareto_points_idx()，支持参数 directions 只输入单个值来表示所有方向都使用该值。

