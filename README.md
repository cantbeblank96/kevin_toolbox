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

- v 1.3.7 （2024-08-01）【new feature】【bug fix】
  - patches
    - for_matplotlib
      - 【new feature】add clear_border_of_axes()，用于清除 ax 中的坐标轴和 ticks。
      - 【new feature】add module color，添加用于处理颜色相关的模块，包含以下函数和属性
        - Color_Format 颜色格式，共有 HEX_STR、RGBA_ARRAY、NATURAL_NAME 三种
        - get_format()，推断所属颜色格式
        - convert_format()，在各种颜色格式之间进行转换
        - generate_color_list()，改进自原来的 for_matplotlib.generate_color_list()，新增了output_format参数用于对颜色格式的控制
      - 添加了测试用例。
    - for_optuna
      - 【bug fix】build_study()，fix bug in line 27，"temp" ==> "temp_ls"
  - nested_dict_list.serializer
    - 【bug fix】write()，fix bug in line 214，新增操作：在保存打包文件前尝试先对目标位置进行清空。
