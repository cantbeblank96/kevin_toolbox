from kevin_toolbox.computer_science.algorithm.registration import UNIFIED_REGISTRY


@UNIFIED_REGISTRY.register(name=":B:class")
class B(object):
    version = "1.0"

    def __init__(self, **kwargs):
        super(B, self).__init__()
        print(kwargs)
