import os
from kevin_toolbox.computer_science.algorithm.registration import Registry

TEST_REGISTRY_3 = Registry(uid="Test_3")

ignore_s = [
    {
        "func": lambda _, __, path: os.path.basename(path) in ["temp", "test", "__pycache__",
                                                               "_old_version"],
        "scope": ["root", "dirs"]
    }
]

TEST_REGISTRY_3.collect_from_paths(
    path_ls=[os.path.join(os.path.dirname(__file__),"here"),os.path.join(os.path.dirname(__file__),"there") ],
    ignore_s=ignore_s,
    b_execute_now=False
)
