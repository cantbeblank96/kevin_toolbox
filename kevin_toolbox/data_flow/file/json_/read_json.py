import os
import json
from kevin_toolbox.data_flow.file.json_.converter import integrate
from kevin_toolbox.computer_science.algorithm.for_nested_dict_list import traverse


def read_json(file_path, converters=None):
    assert os.path.isfile(file_path)
    with open(file_path, 'r') as f:
        content = json.load(f)

    if converters is not None:
        converter = integrate(converters)
        content = traverse(var=[content],
                           match_cond=lambda _, __, ___: True, action_mode="replace",
                           converter=lambda _, x: converter(x),
                           b_traverse_matched_element=True)[0]

    return content
