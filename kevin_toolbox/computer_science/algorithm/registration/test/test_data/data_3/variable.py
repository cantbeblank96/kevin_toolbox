import os
from kevin_toolbox.computer_science.algorithm.registration import Registry

TEST_REGISTRY = Registry(uid="Test")

ignore_s = [
    {
        "func": lambda _, __, path: os.path.basename(path) in ["temp", "test", "__pycache__",
                                                               "_old_version"],
        "scope": ["root", "dirs"]
    }
]

TEST_REGISTRY.collect_from_paths(
    path_ls=[os.path.dirname(__file__), ],
    ignore_s=ignore_s,
    b_execute_now=False
)
