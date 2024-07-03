import os
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.data_flow.file import markdown
from kevin_toolbox.data_flow.file import json_

data_dir = os.path.join(os.path.dirname(__file__), "test_data")


def test_save_images_in_ndl_0():
    from kevin_toolbox.data_flow.file.markdown.test.test_data.for_save_images_in_ndl.data_0.inputs import table_s, \
        setting_s
    expected_dir = os.path.join(data_dir, "for_save_images_in_ndl", "data_0", "expected")
    output_dir = os.path.join(data_dir, "for_save_images_in_ndl", "data_0", "temp")

    res_s = markdown.save_images_in_ndl(
        var=table_s, plot_dir=output_dir + "/plots", doc_dir=output_dir, setting_s=setting_s
    )

    check_consistency(set(os.listdir(output_dir + "/plots")),
                      set(os.listdir(expected_dir + "/plots")))
    check_consistency(res_s,
                      json_.read(file_path=os.path.join(expected_dir, "test.json")))
