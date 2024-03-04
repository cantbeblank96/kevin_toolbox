from kevin_toolbox.computer_science.algorithm.registration.test.test_data.data_5.variable import TEST_REGISTRY_3


@TEST_REGISTRY_3.register()
class Bob_Plus:
    name = ":there:Bob_Plus"
    pass


# 第二种添加方式
for name in [":there:Bob", ":there:bob"]:
    TEST_REGISTRY_3.add(obj=Bob_Plus, name=name, b_force=False, b_execute_now=False)
