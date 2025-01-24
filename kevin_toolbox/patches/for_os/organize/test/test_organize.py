import os
from kevin_toolbox.patches.for_os.organize import group_files_by_timestamp
from kevin_toolbox.data_flow.file import json_
from kevin_toolbox.patches.for_os import remove

data_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "test_data")
temp_dir = os.path.join(data_dir, "temp")
remove(path=temp_dir, ignore_errors=True)
os.makedirs(temp_dir, exist_ok=True)


def test_group_files_by_timestamp():
    for mode in ["m", "a", "c"]:
        res = group_files_by_timestamp(
            suffix_ls=['.jpg', '.mp4', '.png', '.jpeg', '.mov', '.cr2', ".bmp"],
            grouping_rule=("%Y-%m", "%Y_%m_%d"),
            input_dir=os.path.join(data_dir, "data_0"),
            output_dir=os.path.join(temp_dir, mode),
            timestamp_type=mode
        )
        json_.write(content=res, file_path=os.path.join(temp_dir, mode + ".json"), b_use_suggested_converter=True)
