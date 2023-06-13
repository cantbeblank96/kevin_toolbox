from kevin_toolbox.computer_science.algorithm.registration import UNIFIED_REGISTRY
from kevin_toolbox.computer_science.algorithm.registration.test.test_data.data_1.aaa import A


@UNIFIED_REGISTRY.register(name=":B", b_force=True)
def b_func():
    a = A()
    pass
