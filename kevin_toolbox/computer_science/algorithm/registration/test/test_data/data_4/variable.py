import os
from kevin_toolbox.computer_science.algorithm.registration import Registry

TEST_REGISTRY_2 = Registry(uid="Test_2")

ignore_s = [
    {
        "func": lambda _, __, path: os.path.basename(path) in ["temp", "test", "__pycache__",
                                                               "_old_version"],
        "scope": ["root", "dirs"]
    },
    {
        "func": lambda _, __, path: path == __file__,
        "scope": ["files"]
    },  # 相较于 data_3 增加了该排除规则以过滤掉本身调用 collect_from_paths() 的该文件
]

TEST_REGISTRY_2.collect_from_paths(
    path_ls=[os.path.dirname(__file__), ],
    ignore_s=ignore_s,
    b_execute_now=False
)
