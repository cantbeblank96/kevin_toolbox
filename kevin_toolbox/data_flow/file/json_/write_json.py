import os
import json
import copy
from kevin_toolbox.data_flow.file.json_.converter import integrate
from kevin_toolbox.computer_science.algorithm.for_nested_dict_list import traverse


def write_json(content, file_path, sort_keys=False, converters=None, b_use_suggested_converter=False):
    """
        写入 json file

        参数：
            content:                    待写入内容
            file_path
            sort_keys
            converters:                 <list of converters> 对写入内容中每个节点的处理方式
                                            转换器 converter 应该是一个形如 def(x): ... ; return x 的函数，具体可以参考
                                            json_.converter 中已实现的转换器
            b_use_suggested_converter:  <boolean> 是否使用建议的转换器
                                            建议使用 unescape/escape_non_str_dict_key 和 unescape/escape_tuple 这两对转换器，
                                            可以避免因 json 的读取/写入而丢失部分信息。
                                            默认为 False。
                    注意：当 converters 非 None，此参数失效，以 converters 中的具体设置为准
    """
    file_path = os.path.abspath(file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if converters is None and b_use_suggested_converter:
        converters = [unescape_tuple, unescape_non_str_dict_key]

    if converters is not None:
        converter = integrate(converters)
        content = traverse(var=[copy.deepcopy(content)],
                           match_cond=lambda _, __, ___: True, action_mode="replace",
                           converter=lambda _, x: converter(x),
                           b_traverse_matched_element=True)[0]

    with open(file_path, 'w') as f:
        json.dump(content, f, indent=4, ensure_ascii=False, sort_keys=sort_keys)
