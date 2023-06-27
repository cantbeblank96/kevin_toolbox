import os
import copy
import pytest
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.computer_science.algorithm.registration import Registry, UNIFIED_REGISTRY


def test_Registry_0():
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
    # 默认值
    try:
        registry.get(name=":Foo|1.0.4")
    except:
        assert True
    else:
        assert False
    check_consistency(None, registry.get(name=":Foo|1.0.4", default=None))
    # pop
    check_consistency(dict(a=(1, 2)), registry.get(name=":var:a@2", b_pop=True))
    check_consistency([1, 2], registry.get(name=":var:a", b_pop=True))
    check_consistency({"var": {}, "func": {"1": func_1}, "Foo": {"1.0.3": Foo}},
                      registry.database)

    # 检查通过 uid 是否能够获取同一个实例
    registry_2 = Registry(uid="UNIFIED_REGISTRY")
    check_consistency(id(registry), id(registry_2))
    check_consistency(registry.database, registry_2.database)

    # collect_from_paths() of UNIFIED_REGISTRY
    UNIFIED_REGISTRY.clear()
    UNIFIED_REGISTRY.collect_from_paths(path_ls=[os.path.join(os.path.dirname(__file__), "test_data/data_0")],
                                        b_execute_now=True)
    db = copy.deepcopy(UNIFIED_REGISTRY.database)
    check_consistency({"B": {"class": db["B"]["class"]}, "var": {"c": 233}}, db)
    check_consistency("B", db["B"]["class"].__name__)

    #
    UNIFIED_REGISTRY.collect_from_paths(path_ls=[os.path.join(os.path.dirname(__file__), "test_data/data_1")],
                                        b_execute_now=True)
    db = copy.deepcopy(UNIFIED_REGISTRY.database)
    check_consistency({"A": {"1.0": db["A"]["1.0"]}, "B": db["B"], "var": {"c": 233}}, db)
    check_consistency("A", db["A"]["1.0"].__name__)
    check_consistency("b_func", db["B"].__name__)


def test_Registry_1():
    print("test registration.Registry()")

    instances = set(UNIFIED_REGISTRY.instances_of_Registry.keys())

    # 测试实例管理
    a = Registry()
    counter = set(UNIFIED_REGISTRY.instances_of_Registry.keys()).difference(instances)
    assert len(counter) == 1
    counter = list(counter)[0]
    #
    del a
    check_consistency(instances, set(UNIFIED_REGISTRY.instances_of_Registry.keys()))
    #
    a = Registry()
    check_consistency(instances.union({counter, }), set(UNIFIED_REGISTRY.instances_of_Registry.keys()))
    b = Registry(uid=counter + 2)
    check_consistency(instances.union({counter, counter + 2}), set(UNIFIED_REGISTRY.instances_of_Registry.keys()))
    c = Registry()
    check_consistency(instances.union({counter, counter + 2, counter + 1}),
                      set(UNIFIED_REGISTRY.instances_of_Registry.keys()))
    d = Registry()
    check_consistency(instances.union({counter, counter + 2, counter + 1, counter + 3}),
                      set(UNIFIED_REGISTRY.instances_of_Registry.keys()))
    e = Registry(uid=None)
    check_consistency(instances.union({counter, counter + 2, counter + 1, counter + 3}),
                      set(UNIFIED_REGISTRY.instances_of_Registry.keys()))
