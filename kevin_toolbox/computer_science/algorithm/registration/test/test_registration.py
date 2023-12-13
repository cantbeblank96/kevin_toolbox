import os
import copy
import pytest
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.patches import for_os
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
    with pytest.raises(IndexError):
        registry.get(name=":Foo|1.0.4")
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


def test_Registry_collect_from_paths_with_ignore_s():
    print("test registration.Registry.collect_from_paths() with ignore_s")

    UNIFIED_REGISTRY.clear()

    # 构建测试数据
    test_data_path = os.path.join(os.path.dirname(__file__), "test_data/data_2")
    for i in ["aaa/test", "bbb/temp", "eee/ccc/temp", "ddd"]:
        for_os.remove(path=os.path.join(test_data_path, i), ignore_errors=True)
    os.symlink(src=os.path.join(test_data_path, "../data_0"), dst=os.path.join(test_data_path, "ddd"))
    """
    此时 test_data/data_2 目录下的结构为：
        .
        ├── aaa
        │    ├── a_func.py
        │    ├── a.py
        │    ├── __init__.py
        │    └── t_e_s_t.py  # 埋有“钉子”，当导入该模块时会在同一目录下新建一个 test/ 文件夹
        ├── bbb
        │    ├── b_func.py  # 埋有“钉子”，当导入该模块时会在同一目录下新建一个 temp/ 文件夹
        │    └── __init__.py
        ├── ddd -> ../data_0
        ├── eee
        │    └── ccc
        │        ├── c_func.py  # 埋有“钉子”，当导入该模块时会在同一目录下新建一个 temp/ 文件夹
        │        └── __init__.py
        └── __init__.py
    """
    # 忽略的规则
    ignore_s = [
        {
            "func": lambda _, b_is_symlink, path: b_is_symlink or \
                                                  os.path.basename(path) in ["bbb", "eee", "__pycache__"],
            # 排除 bbb 和 eee 以及引用文件夹不进行导入
            "scope": ["root", "dirs"]
        },
        {
            "func": lambda _, __, path: os.path.basename(path) in ["t_e_s_t.py", ],
            # 排除 aaa 文件夹下的 t_e_s_t.py 文件
            "scope": ["files", ]
        },
    ]
    """
    经规则过滤后需要遍历导入的目录结果：
        .
        ├── aaa
        │    ├── a_func.py
        │    ├── a.py   # 这个模块中另外导入了 test_data.data_0.B （如果之前的测试用例没有导入过，则会在本次进行导入）
        │    └── __init__.py
        └── __init__.py
    """

    #
    UNIFIED_REGISTRY.collect_from_paths(path_ls=[test_data_path, ], ignore_s=ignore_s, b_execute_now=True)

    db = copy.deepcopy(UNIFIED_REGISTRY.database)
    if "B" in db:
        db.pop("B")
    check_consistency({"A": {"1.0": db["A"]["1.0"]}, "a_func": db["a_func"]}, db)
    check_consistency("A", db["A"]["1.0"].__name__)
    check_consistency("a_func", db["a_func"].__name__)
    # 检查 ignore_s 匹配的目录是否成功排除
    for i in ["aaa/test", "bbb/temp", "eee/ccc/temp"]:
        assert not os.path.isdir(os.path.join(test_data_path, i))

    # 恢复现场
    for i in ["aaa/test", "bbb/temp", "eee/ccc/temp", "ddd"]:
        for_os.remove(path=os.path.join(test_data_path, i), ignore_errors=True)
