import pytest
import os
from kevin_toolbox.patches import for_os
from kevin_toolbox.data_flow.file import json_


def test_remove():
    print("test for_os.remove()")

    temp_dir = os.path.join(os.path.dirname(__file__), "temp")

    # 测试移除文件
    file_path = os.path.join(temp_dir, "test")
    json_.write(content=[1, 2, 3], file_path=file_path)
    assert os.path.isfile(file_path)
    assert for_os.remove(path=file_path)
    assert not os.path.exists(file_path)

    # 移除文件夹
    json_.write(content=[1, 2, 3], file_path=os.path.join(temp_dir, "folder", "233", "test"))
    assert os.path.isdir(temp_dir)
    assert for_os.remove(path=temp_dir)
    assert not os.path.exists(temp_dir)


def test_pack_and_unpack():
    print("test for_os.pack() and for_os.unpack()")

    temp_dir = os.path.join(os.path.dirname(__file__), "temp")
    for_os.remove(path=temp_dir, ignore_errors=True)
    os.makedirs(temp_dir, exist_ok=True)

    # 测试打包
    file_ls = [
        os.path.join("pack", "233.json"),
        os.path.join("pack", "dir_0", "666.json"),
    ]
    folder_ls = [
        os.path.join("pack", "dir_0", "folder"),
        os.path.join("pack", "dir_1"),
    ]
    for file in file_ls:
        json_.write(content=[1, 2, 3], file_path=os.path.join(temp_dir, file), )
    for folder in folder_ls:
        os.makedirs(os.path.join(temp_dir, folder), exist_ok=True)

    # 使用 tarfile
    from kevin_toolbox.patches.for_os.pack import BACKEND
    BACKEND.clear()
    BACKEND.append("tarfile")
    for_os.pack(source=os.path.join(temp_dir, "pack"), target=os.path.join(temp_dir, "pack_tarfile.tar"))
    # 使用 os
    BACKEND.clear()
    BACKEND.append("os")
    for_os.pack(source=os.path.join(temp_dir, "pack"), target=os.path.join(temp_dir, "pack_os.tar"))

    # 测试解压
    # 使用 tarfile
    from kevin_toolbox.patches.for_os.unpack import BACKEND
    BACKEND.clear()
    BACKEND.append("tarfile")
    for_os.unpack(source=os.path.join(temp_dir, "pack_os.tar"), target=os.path.join(temp_dir, "unpack_tarfile"))
    # 使用 os
    BACKEND.clear()
    BACKEND.append("os")
    for_os.unpack(source=os.path.join(temp_dir, "pack_tarfile.tar"), target=os.path.join(temp_dir, "unpack_os"))

    # 验证一致性
    for file in file_ls:
        assert os.path.isfile(os.path.join(temp_dir, "unpack_tarfile", file))
        assert os.path.isfile(os.path.join(temp_dir, "unpack_os", file))
    for folder in folder_ls:
        assert os.path.isdir(os.path.join(temp_dir, "unpack_tarfile", folder))
        assert os.path.isdir(os.path.join(temp_dir, "unpack_os", folder))

    # 恢复现场
    for_os.remove(path=temp_dir, ignore_errors=True)
