import pytest
from kevin.patches.for_test import check_consistency

import os

from kevin.data_flow.file import json_


@pytest.mark.parametrize("content, converters",
                         zip([[{123: 123, -1: -1, 1.23: 1.23, -1.000: -1.0, "1.2.3": None}], ],
                             [[json_.converter.convert_dict_key_to_number], ]))
def test_json(content, converters):
    print("test file.json_")

    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "test_data/temp/data_0.json")
    json_.write(content=content, file_path=file_path)
    content1 = json_.read(file_path=file_path, converters=converters)
    check_consistency(content, content1)
