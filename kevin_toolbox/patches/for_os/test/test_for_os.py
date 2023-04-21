import pytest
import os
from kevin_toolbox.patches import for_os
from kevin_toolbox.data_flow.file import json_


def test_remove():
    print("test for_os.remove()")

    temp_dir = f'{os.path.split(__file__)[0]}/temp'

    # 测试移除文件
    file_path = os.path.join(temp_dir, "test")
    json_.write(content=[1, 2, 3], file_path=file_path)
    assert os.path.isfile(file_path)
    assert for_os.remove(path=file_path)
    assert not os.path.exists(file_path)

    # 移除文件夹
    json_.write(content=[1, 2, 3], file_path=os.path.join(temp_dir, "folder", "233", "test"))
    assert os.path.isdir(temp_dir)
    assert for_os.remove(path=temp_dir)
    assert not os.path.exists(temp_dir)
