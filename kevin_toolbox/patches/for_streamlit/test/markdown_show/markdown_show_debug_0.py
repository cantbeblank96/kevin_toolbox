import os
import streamlit as st
import sys

root_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))
sys.path.insert(0, root_dir)
from kevin_toolbox.patches.for_streamlit import markdown

"""
bug：
    在 st.expander 中使用 markdown.show() 显示表格时，
    报错 streamlit.errors.StreamlitAPIException: Expanders may not be nested inside other expanders.

产生原因：
    在 streamlit<=1.38.0 下（截止2024-09-23最新版本），禁止在 st.expander 下嵌套使用 st.expander，而在 markdown.show_table() 显示表格时，
    有使用 st.expander 去包裹表格，这导致了嵌套的出现。具体参看：https://docs.streamlit.io/develop/api-reference/layout/st.expander
    
解决方式：
    去除 markdown.show_table() 内对 st.expander 的使用。改而使用 st.tabs 去包裹表格。
"""

st.write(f'## Warped by st.expander')

file_path = os.path.join(root_dir, "kevin_toolbox/patches/for_streamlit/test/test_data/data_0.md")

brief = open(file_path, 'r').read()

with st.expander(label="233", expanded=True):
    markdown.show(brief, doc_dir=os.path.dirname(file_path))
