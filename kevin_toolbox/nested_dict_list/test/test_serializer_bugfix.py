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
