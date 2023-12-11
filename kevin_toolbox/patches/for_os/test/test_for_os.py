import pytest
import os
import copy
import itertools
from kevin_toolbox.patches import for_os
from kevin_toolbox.patches.for_test import check_consistency
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


class Test_walk:

    @staticmethod
    def build_data():
        """
            在 test/test_data 文件夹下构建如下目录结构：
                temp
                ├── a
                │   ├── 233_link -> link to temp/b/233.png
                │   ├── 444_link.jpg -> link to temp/b/d/444.jpg
                │   ├── d_link/ -> link to temp/b/d/
                │   └── README.md
                └── b
                    ├── 233.png
                    ├── c
                    │   ├── e
                    │   │   ├── f/
                    │   │   └── g/
                    │   └── temp
                    │       └── 666.json
                    └── d
                        ├── 444.jpg
                        └── 555.txt
        """
        temp_dir = os.path.join(os.path.dirname(__file__), "test_data", "test_data", "temp")
        for_os.remove(path=temp_dir, ignore_errors=True)
        os.makedirs(temp_dir, exist_ok=True)
        # 
        for i in ["b/233.png", "b/c/temp/666.json", "b/c/e/f", "b/c/e/g", "b/d/444.jpg", "b/d/555.txt", "a/README.md"]:
            if len(os.path.basename(i).split(".")) > 1:
                json_.write(file_path=os.path.join(temp_dir, i), content=[i])
            else:
                os.makedirs(os.path.join(temp_dir, i), exist_ok=True)
        # 创建软连接
        os.symlink(src=os.path.join(temp_dir, "b/d/444.jpg"), dst=os.path.join(temp_dir, "a/444_link.jpg"))
        os.symlink(src=os.path.join(temp_dir, "b/233.png"), dst=os.path.join(temp_dir, "a/233_link"))
        os.symlink(src=os.path.join(temp_dir, "b/d"), dst=os.path.join(temp_dir, "a/d_link"), target_is_directory=True)

        return temp_dir

    def test_consistency_with_os_walk(self):
        """
            测试基础功能与 os.walk() 的一致性
        """
        # 准备测试数据
        temp_dir = self.build_data()
        top_ls = [temp_dir]
        for root, dirs, files in os.walk(temp_dir):
            top_ls.extend(os.path.join(root, dir) for dir in dirs)
        #
        for top, topdown, followlinks in itertools.product(top_ls, [True, False], [True, False]):
            gt = [list(i) for i in os.walk(top, topdown=topdown, followlinks=followlinks)]
            res = [list(i) for i in for_os.walk(top, topdown=topdown, followlinks=followlinks)]
            check_consistency(gt, res)

    def test_ignore_s_0(self):
        """
            测试 ignore_s 参数
        """
        # 准备测试数据
        temp_dir = self.build_data()
        #
        ignore_s = [
            {
                "func": lambda _, __, path: os.path.basename(path) in ["temp", "g"],
                "scope": ["root", "dirs"]
            },
            {
                "func": lambda _, b_is_symlink, path: not b_is_symlink and os.path.basename(path).startswith("d"),
                "scope": ["root", ]
            },
            {
                "func": lambda _, b_is_symlink, path: b_is_symlink or not path.endswith((".png", ".jpg", ".md")),
                "scope": ["files", ]
            }
        ]
        """
        按照规则进行排除后，需要遍历的部分：
            temp
            ├── a
            │   ├── d_link/ -> link to temp/b/d/    (当 followlinks=True 时深入去遍历)
            │   └── README.md
            └── b
                ├── 233.png
                ├── c
                │   └── e
                │       └── f/
                └── d/ （只在 dirs 中输出，不深入去遍历）
        """
        gt = {
            # <root>: {"dirs": set(<dirs>), "files": set(<files>)}
            temp_dir: {"dirs": {"a", "b"}, "files": set()},
            os.path.join(temp_dir, "a"): {"dirs": {"d_link"}, "files": {"README.md"}},
            os.path.join(temp_dir, "a", "d_link"): {"dirs": set(), "files": {"444.jpg"}},
            os.path.join(temp_dir, "b"): {"dirs": {"c", "d"}, "files": {"233.png"}},
            os.path.join(temp_dir, "b", "c"): {"dirs": {"e"}, "files": set()},
            os.path.join(temp_dir, "b", "c", "e"): {"dirs": {"f"}, "files": set()},
            os.path.join(temp_dir, "b", "c", "e", "f"): {"dirs": set(), "files": set()},
        }
        for topdown, followlinks in itertools.product([True, False], [True, False]):
            res = dict()
            for root, dirs, files in for_os.walk(temp_dir, topdown=topdown, followlinks=followlinks, ignore_s=ignore_s):
                res[root] = {"dirs": set(dirs), "files": set(files)}
            gt_ = copy.deepcopy(gt)
            if not followlinks:
                gt_.pop(os.path.join(temp_dir, "a", "d_link"))
            check_consistency(gt_, res)
