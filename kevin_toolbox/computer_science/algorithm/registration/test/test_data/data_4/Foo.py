from kevin_toolbox.computer_science.algorithm.registration.test.test_data.data_4.variable import TEST_REGISTRY_2


# 第一种添加方式
@TEST_REGISTRY_2.register()
class Foo:
    name = ":class:Foo"
    pass
