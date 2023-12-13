from kevin_toolbox.computer_science.algorithm.registration import UNIFIED_REGISTRY
from kevin_toolbox.computer_science.algorithm.registration.test.test_data.data_1.aaa import A


@UNIFIED_REGISTRY.register(name=":ccc", b_force=True)
def c_func():
    a = A()
    pass


import os

os.makedirs(os.path.join(os.path.join(os.path.dirname(__file__), "temp")), exist_ok=True)
