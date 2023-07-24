import os
import pytest
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.data_flow.file import json_


def test_read_and_write_0():
    print("test json_.read() and json_.write()")

    # for write
    content = [{"ads": [1, 2, 3], "sfdf": 65}, [233, 444]]
    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "test_data/temp/data_3.json")
    json_.write(content=content, file_path=file_path, b_use_suggested_converter=False)

    # for read
    content1 = json_.read(file_path=file_path, b_use_suggested_converter=False)
    check_consistency(content, content1)


def test_read_and_write_1():
    print("test json_.read() and json_.write()")

    # for write
    content = [{123: 123, None: None, "<eval>233": 233, (2, 3, 4): (2, 3, 4)}, 233]
    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "test_data/temp/data_4.json")
    json_.write(content=content, file_path=file_path, b_use_suggested_converter=True)

    # for read
    content1 = json_.read(file_path=file_path, b_use_suggested_converter=True)
    check_consistency(content, content1)
