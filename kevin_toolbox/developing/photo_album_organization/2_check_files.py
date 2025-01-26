import os
from collections import defaultdict
from kevin_toolbox.patches.for_os import find_files_in_dir
from kevin_toolbox.data_flow.file import markdown


def check_files(dir_a, dir_b):
    a_files = find_files_in_dir(input_dir=dir_a, b_relative_path=True)
    b_files = find_files_in_dir(input_dir=dir_b, b_relative_path=True)

    a_file_s=defaultdict(list)
    for i in a_files:
        a_file_s[os.path.basename(i)].append(i)
    b_file_s = defaultdict(list)
    for i in b_files:
        b_file_s[os.path.basename(i)].append(i)

    a_keys = set(a_file_s.keys())
    b_keys = set(b_file_s.keys())
    print(f'a diff b:', markdown.generate_list(var={i: a_file_s[i] for i in a_keys - b_keys}))
    print(f'b diff a:', markdown.generate_list(var={i: b_file_s[i] for i in b_keys - a_keys}))


if __name__ == "__main__":
    while True:
        # 输入目录和文件数量阈值
        input_dir = input("请输入待比较的目录A: ").strip()
        output_dir = input("请输入待比较的目录B: ").strip()

        # 执行合并操作
        check_files(dir_a=input_dir, dir_b=output_dir)

        if input("是否继续？y/n\n") == "n":
            break
