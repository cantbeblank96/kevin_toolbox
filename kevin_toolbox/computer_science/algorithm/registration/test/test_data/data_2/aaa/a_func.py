from kevin_toolbox.computer_science.algorithm.registration import UNIFIED_REGISTRY
from kevin_toolbox.computer_science.algorithm.registration.test.test_data.data_1.aaa import A


@UNIFIED_REGISTRY.register(name=":a_func", b_force=True)
def a_func():
    a = A()
    pass
