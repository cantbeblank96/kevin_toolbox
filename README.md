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

- v 1.3.5 （2024-05-18）【bug fix】【new feature】
  - patches
    - for_os
      - 【new feature】add copy()，无论是文件/目录/软连接都可以使用该函数进行复制。
        - 同时支持follow_symlinks参数用于决定是否跟随符号链接复制其指向的内容，支持remove_dst_if_exists用于决定当目标存在时是否尝试进行移除。
    - for_test
      - 【bug fix】fix bug in check_consistency()，解决了以下问题：
        - 对于含有 np.nan 值的array错误地一律都判断为不相等，修改后将相同位置的 np.nan 值视为相等。
        - require_same_shape=False 时无法正常为不对齐的 可变长度类型 报错。
        - 对于包含 requires_grad=True 的 tensor 的复杂 tuple 异常报错。
    - 添加了对应的测试用例。
  - nested_dict_list
    - 【bug fix】modify temporary file management in write() and read()，加强对写入和读取时创建的临时文件的管理，保证异常退出时能够自动清理临时文件夹。
  - data_flow.file
    - json_
      - 【new feature】modify read()，新增了 file_obj 参数，支持直接从 BytesIO 和 StringIO 中读取json文件。
    - 添加了对应的测试用例。
  - 在更高版本的numpy中已经没有 np.warnings 了，因此将所有 np.warnings 替换为 warnings。

