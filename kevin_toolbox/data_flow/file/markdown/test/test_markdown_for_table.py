import os
import pytest
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.data_flow.file import markdown
from kevin_toolbox.data_flow.file.markdown.test.test_data.for_generate_table.data_s import content_s_ls, param_s_ls, \
    expected_result_ls

data_dir = os.path.join(os.path.dirname(__file__), "test_data")


@pytest.mark.parametrize("content_s, param_s, expected_result",
                         zip(content_s_ls, param_s_ls, expected_result_ls))
def test_generate_table(content_s, param_s, expected_result):
    print("test markdown.generate_table()")

    check_consistency(markdown.generate_table(content_s=content_s, **param_s).strip(), expected_result.strip())


def test_find_tables():
    with open(os.path.join(data_dir, "for_find_tabels", "data_0.md"), 'r') as f:
        assert len(markdown.find_tables(text=f.read())) == 3


@pytest.mark.parametrize("content_s, param_s, expected_result",
                         zip(content_s_ls[:5], param_s_ls[:5], expected_result_ls[:5]))
def test_parse_table_0(content_s, param_s, expected_result):
    print("test markdown.parse_table() and markdown.find_tables()")

    for output_format in ["simple_dict", "complete_dict"]:
        raw_table_ls = markdown.find_tables(text=expected_result)
        assert len(raw_table_ls) == 1
        table_s = markdown.parse_table(raw_table=raw_table_ls[0], output_format=output_format,
                                       b_remove_empty_lines=False,
                                       **{k: v for k, v in param_s.items() if
                                          k in ["orientation", "chunk_size", "chunk_nums"]})
        check_consistency(markdown.generate_table(content_s=table_s, **param_s).strip(), expected_result.strip())


@pytest.mark.parametrize("content_s, param_s, expected_result",
                         zip(content_s_ls[5:6], param_s_ls[5:6], expected_result_ls[5:6]))
def test_parse_table_1(content_s, param_s, expected_result):
    print("test markdown.parse_tables()")

    """
    该例子中含有 f_gen_order_of_values，比较特殊，需要通过 b_remove_empty_lines=True 去除空行，才能保证再次写入的结果和原来保持一致
    """

    for output_format in ["simple_dict", "complete_dict"]:
        raw_table_ls = markdown.find_tables(text=expected_result)
        assert len(raw_table_ls) == 1
        table_s = markdown.parse_table(raw_table=raw_table_ls[0], output_format=output_format,
                                       b_remove_empty_lines=True,
                                       **{k: v for k, v in param_s.items() if
                                          k in ["orientation", "chunk_size", "chunk_nums"]})
        check_consistency(markdown.generate_table(content_s=table_s, **param_s).strip(), expected_result.strip())
