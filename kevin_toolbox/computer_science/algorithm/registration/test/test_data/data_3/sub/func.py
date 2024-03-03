from kevin_toolbox.computer_science.algorithm.registration.test.test_data.data_3.variable import TEST_REGISTRY

# 第二种添加方式
for name in [":func:test_0", ":func:test_1"]:
    TEST_REGISTRY.add(obj=lambda x: 3, name=name, b_force=False, b_execute_now=False)
