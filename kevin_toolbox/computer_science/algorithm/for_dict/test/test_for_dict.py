import pytest
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.computer_science.algorithm import for_dict


def test_deep_update():
    print("test for_nested_dict_list.get_value_by_name()")

    #
    stem = {"a": {"b": [233], "g": 3}}
    patch = {"a": {"b": 444}}
    for_dict.deep_update(stem=stem, patch=patch)
    check_consistency({'a': {'b': 444, 'g': 3}}, stem)

    #
    stem = {'settings': None, 'strategy': None}
    patch = {'strategy': {'__trigger_name': 'epoch'}}
    check_consistency({'settings': None, 'strategy': {'__trigger_name': 'epoch'}},
                      for_dict.deep_update(stem=stem, patch=patch))
