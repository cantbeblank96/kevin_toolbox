import os
import warnings
import pytest
import numpy as np
from kevin_toolbox.patches.for_test import check_consistency
import kevin_toolbox.nested_dict_list as ndl
from kevin_toolbox.nested_dict_list import name_handler, serializer
from kevin_toolbox.computer_science.algorithm.for_dict import deep_update
from kevin_toolbox.patches.for_os import remove

temp_folder = os.path.join(os.path.dirname(__file__), "temp")


def test_write_0():
    print("test serializer.write()")

    warnings.filterwarnings("ignore", category=UserWarning)

    # bug：
    #   在 v1.3.3 前直接使用原始的 node_name 来作为 nodes/ 目录下的文件名，这导致当 node_name 中带有特殊字符时，比如 "/"（在linux下） 和 ":"（在windows下），
    #   将会导致保存失败。
    # fix：
    #   使用 saved_node_name_format 指定生成文件名的方式，默认方式 '{count}_{hash_name}' 可以避免出现特殊字符。

    # bug 复现
    var_ = {"https:/": np.ones((3, 3))}
    with pytest.raises(Exception):
        remove(temp_folder, ignore_errors=True)
        # 使用原始的 node_name 会报错
        serializer.write(var=var_, output_dir=os.path.join(temp_folder, "test_write_0"),
                         saved_node_name_format="{raw_name}")
    remove(temp_folder, ignore_errors=True)
    # 使用新的 saved_node_name_format 不会报错
    serializer.write(var=var_, output_dir=os.path.join(temp_folder, "test_write_0"),
                     saved_node_name_format='{count}_{hash_name}')
    # for read
    res = serializer.read(input_path=os.path.join(temp_folder, "test_write_0.tar"))
    # check
    check_consistency(res, var_)


def test_write_1():
    print("test serializer.write()")

    # bug：
    #   在 v1.3.3 前 processed_s 通过 ndl.set_value() 来逐个节点构建，但是由于根据节点名创建的结果可能和原结构存在差异（详见 ndl.set_value() 中b_force参数的介绍），
    #   因此导致 processed_s 和 var 结构不一致，导致出错。
    # fix：
    #   使用 ndl.copy_() 来创建结构与 var 一致的 processed_s。

    var_ = {"a": {2: 3}}
    remove(temp_folder, ignore_errors=True)
    serializer.write(var=var_, output_dir=os.path.join(temp_folder, "test_write_1"))
    # for read
    res = serializer.read(input_path=os.path.join(temp_folder, "test_write_1.tar"))
    # check
    check_consistency(res, var_)


def test_write_2():
    """
        bug：
          在 v1.4.10 及之前的版本中，对于使用 b_keep_identical_relations=True 设置进行 write() 的情况，需要
          使用 replace_identical_with_reference() 找出 var 中 id 相同的节点，但是该函数的 _forward 中是通过 get_nodes 来获取各层节点，并记录节点的 id
          和 level，这就导致某些节点由于其下具有不同长度的到叶节点的路径，因此节点会同时属于多个 level，最终导致其在 id_to_height_s 中被记录为有多个高度，
          这进一步导致其无法通过后面“具有相同 id 的节点所处的高度应该相同”的检验条件。
        fix：
          修复了 replace_identical_with_reference() 中的 _forward 部分，仅记录每个节点的最大高度。
          去除了“具有相同 id 的节点所处的高度应该相同”的检验条件。
    """

    a = {
        "name": ':for_images:torchvision:Normalize',
        "paras": []
    }
    var = {
        "dataset": a,
        "dataset3": a
    }

    ndl.serializer.write(
        var=var,
        output_dir=os.path.join(temp_folder, "test_write_2"),
        b_pack_into_tar=True, b_keep_identical_relations=True, b_allow_overwrite=True
    )

    res = serializer.read(input_path=os.path.join(temp_folder, "test_write_2.tar"))
    # check
    check_consistency(res, var)


def test_write_3():
    """
        fix：
          记录每个节点的最大高度而非最小高度。由于可能存在父节点和子节点最小高度相等的情况，因此选取最大高度才能表征父节点和子节点的层级关系。
    """

    for _ in range(9):
        transforms_for_train = {
            "settings": [
                # 归一化
                {
                    "name": ':for_images:torchvision:ToTensor',
                    "paras": {}
                }
            ]
        }

        transforms_for_test = {
            "settings": [
                # 归一化
                transforms_for_train["settings"][-1]
            ]
        }

        var = dict()
        var['for_train'] = {
            "dataset": {
                "paras": {
                    "transform": transforms_for_train,
                    "transforms": transforms_for_test
                }
            }
        }

        out_file = ndl.serializer.write(
            var=var,
            output_dir=os.path.join(temp_folder, "test_write_2"),
            settings=[
                {"match_cond": lambda _, idx, value: ndl.name_handler.parse_name(idx)[-1][-1] in ["transform",
                                                                                                  "transforms"],
                 "backend": (":json",)},
                {"match_cond": "<level>-1", "backend": (":skip:simple",)},
            ],
            b_pack_into_tar=False, b_keep_identical_relations=True, b_allow_overwrite=True
        )

        res = serializer.read(input_path=out_file)
        # check
        check_consistency(res, var)
