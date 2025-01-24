import os
import time
from kevin_toolbox.patches.for_os.organize import group_files_by_timestamp

if __name__ == "__main__":
    while True:
        input_dir = input("please input the root path\n")
        output_dir = input("please input the target_path\n")
        #
        grouping_rule = ["%Y", "%Y_%m_%d"]  # "%Y-%m-%d %H:%M:%S" 2016-03-20 11:45:39 #"%a %b"  Sat Mar
        temp = input(f"please input the grouping_rule (default is {' '.join(grouping_rule)})\n")
        if temp != "":
            grouping_rule = temp.split(" ")
        #
        suffix_ls = ['.jpg', '.mp4', '.png', '.jpeg', '.mov', '.cr2', '.bmp']
        temp = input(f"please input the suffix_ls (default is {' '.join(suffix_ls)})\n")
        if temp != "":
            suffix_ls = temp.split(" ")
        timestamp_type = input("分类标准：m for modifytime \n c for createtime\n a for accesstime\n")
        output_dir = os.path.join(output_dir, 'deal' + str(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())))
        group_files_by_timestamp(
            suffix_ls=suffix_ls,
            b_ignore_case=True,
            grouping_rule=grouping_rule,
            input_dir=input_dir,
            output_dir=output_dir, timestamp_type=timestamp_type, b_verbose=True
        )
        if input("是否继续？y/n\n") == "n":
            break
