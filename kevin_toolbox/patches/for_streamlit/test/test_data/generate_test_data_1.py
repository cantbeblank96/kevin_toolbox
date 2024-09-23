import os
from kevin_toolbox.data_flow.file import markdown
from kevin_toolbox.patches.for_os import find_files_in_dir

output_dir = os.path.dirname(__file__)
image_ls = list(find_files_in_dir(input_dir=os.path.join(os.path.dirname(__file__), "images"), suffix_ls=[".jpg"],
                                  b_relative_path=False))

doc = "# 表格示例\n\n"

doc += "## 带图表格\n\n"

table_s = {
    "image": [markdown.generate_link(name=os.path.basename(i), target=os.path.relpath(i, output_dir), type_="image") for
              i in image_ls],
    "image_name": [os.path.basename(i) for i in image_ls]
}

doc += markdown.generate_table(content_s=table_s, orientation="horizontal", chunk_size=3) + "\n\n"

doc += "## 无图表格\n\n"


table_s = {
    "line1": list(range(10)),
    "line2": list(range(5,15))
}

doc += markdown.generate_table(content_s=table_s, orientation="horizontal", chunk_size=5) + "\n\n"

with open(os.path.join(output_dir, "data_1.md"), "w") as f:
    f.write(doc)
