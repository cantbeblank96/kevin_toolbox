import os
import pytest
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.data_flow.file import markdown
from kevin_toolbox.data_flow.file.markdown.table import find_tables, convert_format
from kevin_toolbox.data_flow.file.markdown.test.test_data.for_generate_table.data_s import content_s_ls, param_s_ls, \
    expected_result_ls

data_dir = os.path.join(os.path.dirname(__file__), "test_data")


def test_find_tables_0():
    with open(os.path.join(data_dir, "for_find_tabels", "data_0.md"), 'r') as f:
        text = f.read()
        assert len(find_tables(text=text, b_compact_format=True)) == 3
        table_ls, part_slices_ls, table_idx_ls = find_tables(text=text, b_compact_format=False)
        assert len(part_slices_ls) == 6
        check_consistency(table_idx_ls, [1, 3, 5])


@pytest.mark.parametrize("content_s, param_s, expected_result",
                         zip(content_s_ls[:5], param_s_ls[:5], expected_result_ls[:5]))
def test_find_tables_1(content_s, param_s, expected_result):
    print("test find_tables()")

    for output_format in ["simple_dict", "complete_dict"]:
        table_ls = find_tables(text=expected_result, b_compact_format=True)
        assert len(table_ls) == 1
        content_s = table_ls[0]
        #
        content_s["b_remove_empty_lines"] = False
        for k, v in param_s.items():
            if k in ["orientation", "chunk_size", "chunk_nums"]:
                content_s[k] = v
        content_s = convert_format(content_s=content_s, output_format=output_format)
        check_consistency(markdown.generate_table(content_s=content_s, **param_s).strip(), expected_result.strip())


@pytest.mark.parametrize("content_s, param_s, expected_result",
                         zip(content_s_ls[5:6], param_s_ls[5:6], expected_result_ls[5:6]))
def test_find_tables_2(content_s, param_s, expected_result):
    print("test markdown.find_tables()")

    """
    该例子中含有 f_gen_order_of_values，比较特殊，需要通过 b_remove_empty_lines=True 去除空行，才能保证再次写入的结果和原来保持一致
    """

    for output_format in ["simple_dict", "complete_dict"]:
        table_ls = find_tables(text=expected_result, b_compact_format=True)
        assert len(table_ls) == 1
        content_s = table_ls[0]
        #
        content_s["b_remove_empty_lines"] = True
        for k, v in param_s.items():
            if k in ["orientation", "chunk_size", "chunk_nums"]:
                content_s[k] = v
        content_s = convert_format(content_s=content_s, output_format=output_format)
        check_consistency(markdown.generate_table(content_s=content_s, **param_s).strip(), expected_result.strip())
