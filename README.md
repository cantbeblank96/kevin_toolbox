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

- v 1.4.9 （2025-03-27）【new feature】【bug fix】

  - patches.for_numpy.linalg
    - 【bug fix】fix bug in softmax()，修改 33 行，从减去全局最大值改为减去各个分组内部的最大值，避免全局最大值过大导致某些分组全体数值过小导致计算溢出。
  - patches.for_matplotlib.common_charts.utils
    - modify save_plot()，在最后增加 plt.close() 用于及时销毁已使用完的画布，避免不必要的内存占用。
  - nested_dict_list
    - 【new feature】modify traverse()，增加以下参数以更加精确地控制遍历时的行为：
      - b_skip_repeated_non_leaf_node:  是否跳过重复的非叶节点。
        - 何为重复？在内存中的id相同。
        - 默认为 None，此时将根据 action_mode 的来决定：
          - 对于会对节点进行修改的模式，比如 "remove" 和 "replace"，将设为 True，以避免预期外的重复转换和替换。
          - 对于不会修改节点内容的模式，比如 "skip"，将设为 False。
      - cond_for_repeated_leaf_to_skip：函数列表。在叶节点位置上，遇到满足其中某个条件的重复的元素时需要跳过。
    - 同步修改内部使用了 traverse() 的 get_nodes() 和 copy_() 等函数。
    - 新增了对应的测试用例。
  - data_flow.file.json_
    - 【bug fix】fix bug in write()。
      - bug 归因：在 json_.write() 中通过使用 ndl.traverse() 来找出待转换的元素并进行转换，但是在 v1.4.8 前，该函数默认不会跳过重复（在内存中的id相同）出现的内容。由于该内容的不同引用实际上指向的是同一个，因此对这些引用的分别多次操作实际上就是对该内容进行了多次操作。
      - bug 解决：在后续 v1.4.9 中为 ndl.traverse() 新增了 b_skip_repeated_non_leaf_node 用于控制是否需要跳过重复的引用。我们只需要在使用该函数时，令参数 b_skip_repeated_non_leaf_node=True即可。
