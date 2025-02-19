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

- v 1.4.6 （2025-01-24）【new feature】

  - data_flow.file
    - modify json_.read()，支持输入路径使用 ~ 表示家目录。
    - 【new feature】add excel，该模块用于 excel 表格处理。
      - write_with_matrix()：将矩阵写入到 excel 文件中

  - patches.for_os
    - modify find_files_in_dir()，支持 suffix_ls 设定 None 以表示不进行任何过滤。
    - 【new feature】add organize，该模块用于文件整理。
      - group_files_by_timestamp()：将 input_dir 中的文件按照时间戳信息进行分组，输出到 output_dir 中。
    - 添加了对应的测试用例。
  - env_info
    - 【new feature】add check_validity_and_uninstall()，检查当前机器时间是否超过 expiration_timestamp 指定的有效期，若超过则卸载 package_name 对应的库。
    - 【new feature】add check_version_and_update()，检查当前库的版本，并尝试更新。
    - 以上函数均系从同名脚本中抽取出来。
  - 以上修改，均已添加了对应的测试用例。
  - developing
    - 【new feature】add photo_album_organization，该模块包含一系列整理相册相关的脚本。
      -  0_group_by_timestamp.py ：按照时间戳分组
      -  1_merge_folders.py ：将文件数量较少的目录合并
- v 1.4.7 （）【new feature】【incompatible change】

  - data_flow.file
    - 【new feature】【incompatible change】modify json_.write()，支持使用参数 output_format 设置更复杂的输出格式。同时废弃原来的sort_keys参数。
      - output_format 支持以下输入：
        - "pretty_printed":     通过添加大量的空格和换行符来格式化输出，使输出更易读
        - "minified":           删除所有空格和换行符，使输出更紧凑
        - `<dict/tuple>`：     更加细致的格式设定，比如 `{"indent": 2, ensure_ascii=True}`，如果需要基于已有格式进行微调可以使用以下方式:`("pretty_printed", {"indent": 2, ensure_ascii=True})`
  - computer_science.algorithm.parallel_and_concurrent
    - 【bug fix】【incompatible change】fix bug in multi_thread_execute()，修正了参数timeout无法对每个任务起效的bug，将参数thread_nums更名为worker_nums。
    - 【new feature】add multi_process_execute()，用于多进程执行任务。同样支持timeout设定和进度条显示。
  - patches.for_matplotlib.common_charts
    - modify plot_lines()，添加了 x_ticklabels_name 参数用于自定义x轴的坐标值
  - 以上修改，均已添加了对应的测试用例。
