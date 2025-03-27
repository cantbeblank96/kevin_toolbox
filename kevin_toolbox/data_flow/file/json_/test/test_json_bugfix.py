import os
from io import StringIO
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.data_flow.file import json_

temp_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "test_data/temp")


def test_write_with_repeated_references():
    """
        为了验证下面的 bug 是否已被修复：
            - 当 b_use_suggested_converter=True，若 content 中含有多个重复引用的内容，且该内容需要被转换时，该内容将会被重复多次转换。

        bug 归因：
            在 json_.write() 中通过使用 ndl.traverse() 来找出待转换的元素并进行转换，但是在 v1.4.8 前，该函数默认不会跳过重复（在内存中的id相同）出现的内容。
            由于该内容的不同引用实际上指向的是同一个，因此对这些引用的分别多次操作实际上就是对该内容进行了多次操作。

        bug 解决：
            在后续 v1.4.9 中为 ndl.traverse() 新增了 b_skip_repeated_non_leaf_node 用于控制是否需要跳过重复的引用。我们只需要在使用该函数时，
            令参数 b_skip_repeated_non_leaf_node=True即可。
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
    res_0 = json_.write(content=content, file_path=None, b_use_suggested_converter=True)
    res_1 = json_.read(file_obj=StringIO(res_0), b_use_suggested_converter=False)
    assert "<eval><eval>" not in res_0
    check_consistency(
        res_1,
        {
            "for_val": ["<eval>(224, 224)"],
            "for_test": ["<eval>(224, 224)"]
        }
    )
