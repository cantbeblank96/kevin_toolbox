import pytest
import torch
import numpy as np
from kevin_toolbox.patches.for_test import check_consistency

import os

from kevin_toolbox.data_flow.file import json_


def test_convert_dict_key_to_number():
    print("test converter.convert_dict_key_to_number")

    # for read
    content = [{123: 123, -1: -1, 1.23: 1.23, -1.000: -1.0, "1.2.3": None}]
    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "test_data/temp/data_0.json")
    json_.write(content=content, file_path=file_path)
    content1 = json_.read(file_path=file_path, converters=[json_.converter.convert_dict_key_to_number, ])
    check_consistency(content, content1)


def test_convert_ndarray_to_list():
    print("test converter.convert_ndarray_to_list")

    # for write
    content = [torch.ones(2, 2).cuda(), dict(abc=np.zeros(3), )]
    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "test_data/temp/data_1.json")
    json_.write(
        content=content, file_path=file_path,
        converters=[json_.converter.convert_ndarray_to_list, ]
    )
    content1 = json_.read(file_path=file_path)
    expected = [[[1, 1], [1, 1]], {"abc": [0, 0, 0]}]
    check_consistency(expected, content1)


def test_escape_and_unescape():
    print("test converter.escape/unescape_non_str_dict_key and converter.escape/unescape_tuple")

    # for write
    content = [{123: 123, None: None, "<eval>233": 233, "foo": (2, 3, 4)}, 233]
    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "test_data/temp/data_2.json")
    json_.write(
        content=content, file_path=file_path,
        converters=[json_.converter.escape_non_str_dict_key, json_.converter.escape_tuple]
    )

    # for read
    content1 = json_.read(
        file_path=file_path,
        converters=[json_.converter.unescape_non_str_dict_key, json_.converter.unescape_tuple]
    )
    check_consistency(content, content1)
