import pytest
from kevin_toolbox.patches import for_os
from kevin_toolbox.patches.for_test import check_consistency


@pytest.mark.parametrize("file_name, b_is_path, expected",
                         [
                             ['//data0//b/<?>.md', True, ['<', '?', '>']],
                             ['//data0//b/<?>.md', False, ['/', '/', '/', '/', '/', '<', '?', '>']],
                         ])
def test_find_illegal_chars(file_name, b_is_path, expected):
    print("test for_os.path.find_illegal_chars()")

    res = for_os.path.find_illegal_chars(file_name=file_name, b_is_path=b_is_path)
    check_consistency(res, expected)


@pytest.mark.parametrize("file_name, b_is_path, expected",
                         [
                             ['//data0//b/<?>.md', True, "/data0/b/＜？＞.md"],
                             ['//data0//b/<?>.md', False, "／／data0／／b／＜？＞.md"],
                             ['data0//b/<?>.md', True, "data0/b/＜？＞.md"],
                             ['data0//b/<?>.md', False, "data0／／b／＜？＞.md"],
                         ])
def test_replace_illegal_chars(file_name, b_is_path, expected):
    print("test for_os.path.replace_illegal_chars()")

    res = for_os.path.replace_illegal_chars(file_name=file_name, b_is_path=b_is_path)
    check_consistency(res, expected)
