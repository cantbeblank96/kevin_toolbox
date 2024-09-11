import os
import pytest
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.data_flow.file import markdown
from kevin_toolbox.data_flow.file.markdown.link import find_links, generate_link
from kevin_toolbox.data_flow.file.markdown.test.test_data.for_generate_table.data_s import content_s_ls, param_s_ls, \
    expected_result_ls

data_dir = os.path.join(os.path.dirname(__file__), "test_data")


def test_link_0():
    print("test generate_link() and find_links()")

    text = """
    Here is an image:
    ![This is a picture of a cat](http://example.com/cat.jpg "A cute cat")
    And another one:
    ![This is a picture of a dog](http://example.com/dog.jpg 'A cute dog')
    And one without alt text:
    [](http://example.com/placeholder.jpg)
    And one without title:
    ![<image_name>](<image_path>)
    """

    #
    assert len(find_links(text=text, b_compact_format=True)) == 4
    assert len(find_links(text=text, b_compact_format=True, type_ls=["url", "image"])) == 4
    assert len(find_links(text=text, b_compact_format=True, type_ls=["url"])) == 1
    assert len(find_links(text=text, b_compact_format=True, type_ls=["image"])) == 3

    link_ls, part_slices_ls, link_idx_ls = find_links(text=text, b_compact_format=False)
    text_2 = ""
    for i, part_slices in enumerate(part_slices_ls):
        if i in link_idx_ls:
            link_s = link_ls.pop(0)
            text_2 += generate_link(**link_s)
        else:
            text_2 += text[part_slices[0]:part_slices[1]]

    check_consistency(text_2.replace("'", '"'), text.replace("'", '"'))
