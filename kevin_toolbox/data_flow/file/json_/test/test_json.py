import pytest
import torch
import numpy as np
from kevin_toolbox.patches.for_test import check_consistency

import os

from kevin_toolbox.data_flow.file import json_


@pytest.mark.parametrize("content, converters",
                         zip([[{123: 123, -1: -1, 1.23: 1.23, -1.000: -1.0, "1.2.3": None}], ],
                             [[json_.converter.convert_dict_key_to_number], ]))
def test_json_0(content, converters):
    print("test converters for read")

    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "test_data/temp/data_0.json")
    json_.write(content=content, file_path=file_path)
    content1 = json_.read(file_path=file_path, converters=converters)
    check_consistency(content, content1)


@pytest.mark.parametrize("content, converters, expected",
                         zip([[torch.ones(2, 2).cuda(), dict(abc=np.zeros(3), )], ],
                             [[json_.converter.convert_ndarray_to_list], ],
                             [[[[1, 1], [1, 1]], {"abc": [0, 0, 0]}], ]))
def test_json_1(content, converters, expected):
    print("test converters for write")

    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "test_data/temp/data_1.json")
    json_.write(content=content, file_path=file_path, converters=converters)
    content1 = json_.read(file_path=file_path)
    check_consistency(expected, content1)
