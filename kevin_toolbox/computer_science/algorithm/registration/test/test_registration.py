import os
import pytest
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.computer_science.algorithm.registration import Registry, UNIFIED_REGISTRY


def test_Registry():
    print("test registration.Registry()")

    # init
    registry = Registry(uid="UNIFIED_REGISTRY")

    # add()
    registry.add(obj=[1, 2, dict(a=(1, 2))], name=":var:a")

    # register()
    @registry.register(name=":func:1")
    def func_1():
        pass

    @registry.register()
    class Foo:
        version = "1.0.3"

    check_consistency({"var": {"a": [1, 2, dict(a=(1, 2))]}, "func": {"1": func_1}, "Foo": {"1.0.3": Foo}},
                      registry.database)

    # get()
    check_consistency((1, 2), registry.get(name=":var:a@2:a"))
    check_consistency(func_1, registry.get(name="|func|1"))
    check_consistency(Foo, registry.get(name=":Foo|1.0.3"))
    check_consistency(None, registry.get(name=":Foo|1.0.4", default=None))

    # pop()
    check_consistency([1, 2, dict(a=(1, 2))], registry.pop(name=":var:a"))
    check_consistency({"var": {}, "func": {"1": func_1}, "Foo": {"1.0.3": Foo}},
                      registry.database)

    # 检查通过 uid 是否能够获取同一个实例
    registry_2 = Registry(uid="UNIFIED_REGISTRY")
    check_consistency(id(registry), id(registry_2))
    check_consistency(registry.database, registry_2.database)

    # collect_from() of UNIFIED_REGISTRY
    UNIFIED_REGISTRY.clear()
    UNIFIED_REGISTRY.collect_from(path_ls=[os.path.join(os.path.dirname(__file__), "test_data/data_0")])
    from kevin_toolbox.computer_science.algorithm.registration.test.test_data import data_0
    check_consistency({"B": {"class": data_0.B}, "var": {"c": 233}}, UNIFIED_REGISTRY.database)
    #
    UNIFIED_REGISTRY.collect_from(path_ls=[os.path.join(os.path.dirname(__file__), "test_data/data_1")])
    from kevin_toolbox.computer_science.algorithm.registration.test.test_data.data_1 import aaa, bbb
    check_consistency({"A": {"1.0": aaa.A}, "B": bbb.b_func, "var": {"c": 233}},
                      UNIFIED_REGISTRY.database)
