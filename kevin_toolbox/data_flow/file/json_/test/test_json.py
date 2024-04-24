import os
import io
import pytest
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.data_flow.file import json_

temp_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "test_data/temp")


@pytest.mark.parametrize("content, b_use_suggested_converter, file_name", [
    [[{"ads": [1, 2, 3], "sfdf": 65}, [233, 444]], False, "data_3.json"],
    [[{123: 123, None: None, "<eval>233": 233, (2, 3, 4): (2, 3, 4)}, 233], True, "data_4.json"]
])
def test_read_and_write(content, b_use_suggested_converter, file_name):
    print("test json_.read() and json_.write()")

    # for write
    file_path = os.path.join(temp_dir, file_name)
    json_.write(content=content, file_path=file_path, b_use_suggested_converter=b_use_suggested_converter)

    # for read
    content1 = json_.read(file_path=file_path, b_use_suggested_converter=b_use_suggested_converter)
    check_consistency(content, content1)
    #   by file_obj: BytesIO
    with open(file_path, "rb") as f:
        content2 = f.read()
    content2 = json_.read(file_obj=io.BytesIO(content2), b_use_suggested_converter=True)
    check_consistency(content, content2)
    #   by file_obj: StringIO
    with open(file_path, "r") as f:
        content3 = f.read()
    content3 = json_.read(file_obj=io.StringIO(content3), b_use_suggested_converter=True)
    check_consistency(content, content3)
