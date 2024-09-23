import os
import streamlit as st
import sys

root_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))
sys.path.insert(0, root_dir)
from kevin_toolbox.patches.for_streamlit import markdown

"""
bug：
    在 markdown.show_table() 的 line 56 和 line 25 中对 show_image() 和 st.markdown 的函数参数写错，导致在显示无图表格时反而报错。
"""

st.write(f'## Warped by st.expander')

file_path = os.path.join(root_dir, "kevin_toolbox/patches/for_streamlit/test/test_data/data_1.md")

brief = open(file_path, 'r').read()

markdown.show(brief, doc_dir=os.path.dirname(file_path))
