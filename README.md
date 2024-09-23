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

- v 1.4.1 （2024-09-23）【bug fix】【new feature】 
  - patches
    - for_streamlit.markdown
      - 【bug fix】fix bug in show_table()，将原来的使用 st.expander 去包裹表格，改为使用 st.tabs 去包裹表格，避免在 streamlit<=1.38.0 下（截止2024-09-23最新版本），因为 st.expander 嵌套使用而造成的报错。具体参看：https://docs.streamlit.io/develop/api-reference/layout/st.expander
      - 【bug fix】fix bug in show_table()，修复在 line 56 和 line 25 中对 show_image() 和 st.markdown 的函数参数写错，导致在显示无图表格时反而报错的问题。
      - 增加了测试用例。

    - for_matplotlib.common_charts
      - 【new feature】 add para replace_zero_division_with to plot_confusion_matrix()，新增参数 replace_zero_division_with 用于指定在normalize时引发除0错误的矩阵元素要使用何种值进行替代。
      - 增加了测试用例。


