from kevin_toolbox.computer_science.algorithm.registration.test.test_data.data_5.variable import TEST_REGISTRY_3


@TEST_REGISTRY_3.register()
class Alex_Plus:
    name = ":here:Alex_Plus"
    pass


# 第二种添加方式
for name in [":here:Alex", ":here:alex"]:
    TEST_REGISTRY_3.add(obj=Alex_Plus, name=name, b_force=False, b_execute_now=False)
