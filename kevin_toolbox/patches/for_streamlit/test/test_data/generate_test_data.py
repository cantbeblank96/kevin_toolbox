import os
from kevin_toolbox.data_flow.file import markdown
from kevin_toolbox.patches.for_os import find_files_in_dir

output_dir = os.path.dirname(__file__)
image_ls = list(find_files_in_dir(input_dir=os.path.join(os.path.dirname(__file__), "images"), suffix_ls=[".jpg"],
                                  b_relative_path=False))

doc = "# 表格示例\n\n"

raw_table_s = {
    "image": [markdown.generate_link(name=os.path.basename(i), target=os.path.relpath(i, output_dir), type_="image") for
              i in image_ls],
    "image_name": [os.path.basename(i) for i in image_ls]
}

for b_image_first in [True, False]:
    doc += f"## b_image_first:{b_image_first}\n\n"
    table_s = {k: raw_table_s[k] for k in (["image", "image_name"] if b_image_first else ["image_name", "image"])}
    for orientation in ["horizontal", "vertical"]:
        doc += f"### orientation:{orientation}\n\n"
        for chunk_size in [None, 1, 2, 3, 4]:
            doc += f"chunk_size: {chunk_size}\n\n"
            doc += markdown.generate_table(content_s=table_s, orientation=orientation, chunk_size=chunk_size) + "\n\n"
        for chunk_nums in [1, 2, 3, 4]:
            doc += f"chunk_nums: {chunk_nums}\n\n"
            doc += markdown.generate_table(content_s=table_s, orientation=orientation, chunk_nums=chunk_nums) + "\n\n"

with open(os.path.join(output_dir, "data_0.md"), "w") as f:
    f.write(doc)
