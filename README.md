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

- v 1.2.4 （2023-08-14）【new feature】【bug fix】
  - nested_dict_list
    - 【bug fix】fix backend :skip:simple，修复了不支持 None 类型值的问题。
    - 【new feature】modify write()，添加了参数以支持控制对写入过程中正确性与完整性的要求的严格程度，目前支持三种可选值，分别对应枚举类型 Strictness_Level 中的三个取值：
      - "high" / Strictness_Level.COMPLETE        所有节点均有一个或者多个匹配上的 backend， 且第一个匹配上的 backend 就成功写入。
      - "normal" / Strictness_Level.COMPATIBLE    所有节点均有一个或者多个匹配上的 backend， 但是首先匹配到的 backend 写入出错，使用其后再次匹配到的其他 backend 能够成功写入
      - "low" / Strictness_Level.IGNORE_FAILURE   匹配不完整，或者某些节点尝试过所有匹配到 的 backend 之后仍然无法写入
      - 默认值是 "normal"。
      - 添加了对应的测试用例。
    - 【bug fix】fix bug in backend :skip:simple and :json，修复了 writable() 中 cache 不能及时更新的问题。
  - 使用 `with pytest.raises(<Error>) ` 来代替测试用例中的 try else 方式来捕抓异常
