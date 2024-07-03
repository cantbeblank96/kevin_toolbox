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

- v 1.3.6 （2024-07-03）【new feature】
  - patches
    - for_os
      - 【new feature】add find_files_in_dir()，找出目录下带有给定后缀的所有文件的生成器。
    - for_os.path
      - 【new feature】add find_illegal_chars()，找出给定的文件名/路径中出现了哪些非法符号。
      - 【new feature】add replace_illegal_chars()，将给定的文件名/路径中的非法符号替换为合法形式。
    - for_matplotlib
      - 【new feature】add module common_charts，新增模块——常用图表，该模块下包含以下函数：
        - plot_bars()，绘制柱状图
        - plot_scatters()，绘制散点图
        - plot_lines()，绘制折线图
        - plot_distribution()，绘制分布图
        - plot_scatters_matrix()，绘制散点图矩阵（常用于多变量关系分析）
        - plot_confusion_matrix()，绘制混淆矩阵（常用于混淆矩阵、相关性矩阵、特征图可视化）
    - 添加了测试用例。
  - data_flow.file
    - markdown
      - 【new feature】add save_images_in_ndl()，将ndl结构叶节点下的图片对象保存到 plot_dir 中，并替换为该图片的markdown链接。
        - 便于对表格中的图片或者列表中的图片进行保存和替换。
      - 【new feature】add find_tables()，用于从文本中找出markdown格式的表格，并以二维数组的列表形式返回。
      - 【new feature】add parse_table()，将二维数组形式的表格（比如find_tables()的返回列表的元素），解析成指定的格式。
    - kevin_notation
      - 【bug fix】fix bug in Kevin_Notation_Writer，增加检验写入的列的元素数量是否一致，不一致时进行报错。
      - 【bug fix】fix bug in write()，避免对输入参数 metadata 中的内容进行意料之外的改动。
  - nested_dict_list
    - add para b_allow_override to serializer.write to allow overwriting，增加参数用于允许强制覆盖已有文件。
  - computer_science.algorithm
    - pareto_front
      - 【new feature】add Optimum_Picker，帕累托最优值选取器。
        - 记录并更新帕累托最优值
        - 同时支持监控以下行为，并触发设定的执行器，详见参数 trigger_for_new 和 trigger_for_out。
                              - 新加值是一个新的帕累托最优值
                              - 抛弃一个不再是最优的旧的最优值
    - statistician
      - 【new feature】add Accumulator_for_Ndl，适用于 ndl 结构的统计器。
      - 【bug fix】fix bug in Accumulator_Base._init_var()
      - 【new feature】modify Average_Accumulator，在 add() 中新增了 weight 参数用于计算带权重的平均值
      - modify Exponential_Moving_Average，add_sequence() 不再支持 weight_ls 参数，让该接口与其他类更加一致。
    - 添加了测试用例。
