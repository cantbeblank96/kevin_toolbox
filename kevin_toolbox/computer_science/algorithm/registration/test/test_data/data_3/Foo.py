from kevin_toolbox.computer_science.algorithm.registration.test.test_data.data_3.variable import TEST_REGISTRY


# 第一种添加方式
@TEST_REGISTRY.register()
class Foo:
    name = ":class:Foo"
    pass
