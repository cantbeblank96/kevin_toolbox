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

- v 1.4.11 （2025-04-16）【bug fix】

  - nested_dict_list
    - 【bug fix】fix bug in value_parser.replace_identical_with_reference()
      - bug 描述：该函数的 _forward 中是通过 get_nodes 来获取各层节点，并记录节点的 id 和 level，这就导致某些节点由于其下具有不同长度的到叶节点的路径，因此节点会同时属于多个 level，最终导致其在 id_to_height_s 中被记录为有多个高度，这进一步导致其无法通过后面“具有相同 id 的节点所处的高度应该相同”的检验条件。
      - 解决：
        - 修复了 replace_identical_with_reference() 中的 _forward 部分，仅记录每个节点的最大高度。
        - 去除了“具有相同 id 的节点所处的高度应该相同”的检验条件。
  - computer_science.algorithm.redirector
    - 【bug fix】fix bug in Redirectable_Sequence_Fetcher，将 _randomly_idx_redirector 中的 rng.choices 改为 rng.choice
  - 添加了对应的测试用例。

