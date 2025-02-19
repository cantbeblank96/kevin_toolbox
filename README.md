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

- v 1.4.7 （2025-02-19）【new feature】【bug fix】【incompatible change】

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
