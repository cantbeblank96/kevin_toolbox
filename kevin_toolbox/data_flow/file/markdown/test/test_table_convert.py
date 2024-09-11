import os
import pytest
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.data_flow.file.markdown.table import convert_format, get_format, Table_Format
from kevin_toolbox.data_flow.file.markdown.test.test_data.for_generate_table.data_s import content_s_ls, param_s_ls, \
    expected_result_ls


def test_generate_table():
    print("test markdown.convert_format()")

    content_s = {'y/n': ['False', 'False', 'False', 'False', 'False', 'True', 'True', 'True', 'True', 'True'],
                 'a': ['5', '8', '7', '6', '9', '2', '1', '4', '0', '3'],
                 'b': ['', '', '', '', '', '6', '4', ':', '2', '8']}

    temp_s = {
        Table_Format.SIMPLE_DICT: [content_s, ],
        Table_Format.COMPLETE_DICT: [],
        Table_Format.MATRIX: []
    }

    for src_f, dst_f in [
        (Table_Format.SIMPLE_DICT, Table_Format.COMPLETE_DICT),
        (Table_Format.COMPLETE_DICT, Table_Format.SIMPLE_DICT),
        (Table_Format.SIMPLE_DICT, Table_Format.MATRIX),
        (Table_Format.MATRIX, Table_Format.SIMPLE_DICT),
        (Table_Format.COMPLETE_DICT, Table_Format.MATRIX),
        (Table_Format.MATRIX, Table_Format.COMPLETE_DICT)
    ]:
        src = temp_s[src_f][-1]
        assert get_format(content_s=src) is src_f
        #
        dst = convert_format(content_s=src, output_format=dst_f)
        temp_s[dst_f].append(dst)

    for v in temp_s.values():
        check_consistency(*v)
