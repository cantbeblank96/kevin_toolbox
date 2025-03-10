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

- v 1.4.8 （2025-03-06）【new feature】【refactor】

  - 【new feature】network，新增网络模块。
    - 该模块包含网络访问相关的函数：
      - get_response()，获取 url 的响应。
      - fetch_metadata()，从 URL/response 中获取文件名、后缀（扩展名）、大小等元信息。
      - fetch_content()，从 URL/response 中获取内容。
      - download_file()，下载文件。
  - env_info
    - modify Env_Vars_Parser.parse()，新增 default 参数用于支持解释失败时候返回默认值。
  - computer_science.algorithm
    - 【refactor】【new feature】decorator，从 developing 中将装饰器相关模块整合到 cs.algorithm 中。
      - 该目录目前包含以下函数：
        - retry()，在函数执行失败时，等待一定时间后重试多次。
        - restore_original_work_path()，在运行函数 func 前备份当前工作目录，并在函数运行结束后还原到原始工作目录。
    - registration
      - 【new feature】add Serializer_for_Registry_Execution，用于对基于 Registry 中成员构建的执行过程进行序列化和反序列化操作。
  - nested_dict_list.serializer
    - modify write()，增加返回值，返回保存到的路径。
  - patches.for_matplotlib
    - 【new feature】add COMMON_CHARTS，增加该注册器用于管理 common_charts 模块中的方法。
    - common_charts
      - 为所有plot_xx函数增加了注释和测试用例。
      - 为所有plot_xx函数增加以下参数：
        - b_generate_record：是否保存函数参数为档案。
          - 默认为 False，当设置为 True 时将会把函数参数保存成 [output_path].record.tar。
          - 后续可以使用 plot_from_record() 函数或者 Serializer_for_Registry_Execution 读取该档案，并进行修改和重新绘制。
          - 该参数仅在 output_dir 和 output_path 非 None 时起效。
        - output_path：图片输出路径。
          - 支持直接指定图片要保存的路径，在原有的通过 output_dir 和 title 自动生成路径的方式之外，提供了另一个指定的方式。
      - 【new feature】add plot_from_record，从保存的档案 .record.tar 文件中恢复并绘制图像。
