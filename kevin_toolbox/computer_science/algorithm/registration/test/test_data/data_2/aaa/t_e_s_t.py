import os
from kevin_toolbox.computer_science.algorithm.registration import UNIFIED_REGISTRY


@UNIFIED_REGISTRY.register(name=":a:test", b_force=True)
def test():
    print("233")


os.makedirs(os.path.join(os.path.join(os.path.dirname(__file__), "test")), exist_ok=True)
