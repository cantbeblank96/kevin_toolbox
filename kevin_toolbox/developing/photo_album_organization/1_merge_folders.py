import os
import shutil
from datetime import datetime
from kevin_toolbox.patches.for_os import copy

"""
寻找输入目录input_dir下形如 input_dir/**/%Y_%m_%d 的文件夹，
    比如 input_dir/233/2024_05_26 和 input_dir/233/2023_08_15，
将其中文件数量少于给定值的文件夹合并到 input_dir/**/%Y_%m 中，
    比如  input_dir/233/2023_08
"""


def is_date_folder(folder_name):
    """判断文件夹名称是否符合 %Y_%m_%d 格式"""
    try:
        datetime.strptime(folder_name, "%Y_%m_%d")
        return True
    except ValueError:
        return False


def merge_folders(input_dir, file_threshold):
    """
    合并 input_dir 下符合条件的日期文件夹。

    Args:
        input_dir (str): 输入的根目录。
        file_threshold (int): 文件数量的阈值。
    """
    for root, dirs, files in os.walk(input_dir):
        for folder_name in dirs:
            dir_path = os.path.join(root, folder_name)

            # 如果文件夹名符合日期格式 %Y_%m_%d
            if is_date_folder(folder_name):
                file_count = len(os.listdir(dir_path))

                if file_count < file_threshold:
                    # 解析 %Y_%m_%d 格式
                    year_month = datetime.strptime(folder_name, "%Y_%m_%d").strftime("%Y_%m")
                    target_folder = os.path.join(root, year_month)
                    os.makedirs(target_folder, exist_ok=True)

                    # 移动文件到目标文件夹
                    for file_name in os.listdir(dir_path):
                        src_file = os.path.join(dir_path, file_name)
                        dst_file = os.path.join(target_folder, file_name)
                        copy(src_file, dst_file)

                    #
                    temp_dir = os.path.join(root, "temp")
                    os.makedirs(temp_dir, exist_ok=True)
                    shutil.move(dir_path, temp_dir)


if __name__ == "__main__":
    while True:
        # 输入目录和文件数量阈值
        input_dir = input("请输入根目录路径: ").strip()
        file_threshold = int(input("请输入文件数量阈值: ").strip())

        # 执行合并操作
        merge_folders(input_dir, file_threshold)
        print("合并完成！")

        if input("是否继续？y/n\n") == "n":
            break
