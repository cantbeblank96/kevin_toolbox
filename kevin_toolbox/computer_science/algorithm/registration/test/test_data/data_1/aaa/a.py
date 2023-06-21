from kevin_toolbox.computer_science.algorithm.registration import UNIFIED_REGISTRY
from kevin_toolbox.computer_science.algorithm.registration.test.test_data.data_0 import B


@UNIFIED_REGISTRY.register()
class A(B):
    version = "1.0"

    def __init__(self, **kwargs):
        super(A, self).__init__(**kwargs)


if __name__ == '__main__':
    A(foo=233)