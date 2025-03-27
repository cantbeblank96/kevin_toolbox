import os
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.nested_dict_list import serializer

temp_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "test_data/temp")


def test_write_with_repeated_references():
    """
        为了验证下面的 bug 是否已被修复：
            - 当待写入内容 content 中含有多个重复引用，且该内容需要被转换时，该内容将会被重复多次转换。

        bug 归因和解决方法：
            问题出现其中调用 json_.write() 的过程，而 json_.write() 中的问题又源自于 ndl.traverse()，具体参见
            kevin_toolbox/data_flow/file/json_/test/test_json_bugfix.py。
    """

    # data
    transforms_s = [
        (224, 224)
    ]
    content = {
        "for_val": transforms_s,
        "for_test": transforms_s
    }

    #
    out_file = serializer.write(
        var=content,
        output_dir=os.path.join(temp_dir, "test_write_with_repeated_references"),
        b_pack_into_tar=False,
        b_allow_overwrite=True
    )
    res = serializer.read(input_path=out_file)
    check_consistency(
        res,
        content
    )
