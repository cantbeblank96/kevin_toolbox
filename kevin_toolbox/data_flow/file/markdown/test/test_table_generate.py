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
