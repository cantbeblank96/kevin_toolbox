import os
import streamlit as st
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
sys.path.insert(0, root_dir)
print(root_dir)
from kevin_toolbox.patches.for_streamlit import markdown

st.write(f'## Visualization')

file_path = os.path.join(root_dir, "kevin_toolbox/patches/for_streamlit/test/test_data/data_0.md")

brief = open(file_path, 'r').read()
markdown.show(brief, doc_dir=os.path.dirname(file_path))
