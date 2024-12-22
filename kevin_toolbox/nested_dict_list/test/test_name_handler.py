from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.nested_dict_list.name_handler import escape_node, parse_name, \
    build_name


def test_escape_node():
    print("test name_handler.escape_node()")

    x = "new|model:acc@step=4"

    # 转义
    res = escape_node(node=x, b_reversed=False, times=4)
    check_consistency(r"new\\\\|model\\\\:acc\\\\@step=4", res)

    # 反转义
    res = escape_node(node=res, b_reversed=True, times=1)
    check_consistency(r"new\\\|model\\\:acc\\\@step=4", res)
    res = escape_node(node=res, b_reversed=True, times=-1)
    check_consistency(x, res)

    # 非法参数报错
    try:
        escape_node(node=x, b_reversed=False, times=-1)
    except:
        pass
    else:
        raise NotImplementedError(f'Illegal parameter error failure')


def test_parse_name():
    print("test name_handler.parse_name()")

    x = "var:strategy:\:settings\@for_all\:lr@100"
    root_node, method_ls, node_ls = parse_name(name=x, b_de_escape_node=True)
    check_consistency(root_node, "var")
    check_consistency(method_ls, [":", ":", "@"])
    check_consistency(node_ls, ["strategy", ":settings@for_all:lr", "100"])


def test_build_name():
    print("test name_handler.build_name()")

    x = "var:strategy:\:settings\@for_all\:lr@100"
    root_node, method_ls, node_ls = parse_name(name="var:strategy:\:settings\@for_all\:lr@100", b_de_escape_node=True)
    res = build_name(root_node=root_node, method_ls=method_ls, node_ls=node_ls, b_escape_node=True)
    check_consistency(x, res)
    #
    root_node, method_ls, node_ls = parse_name(name="var:strategy:\:settings\@for_all\:lr@100", b_de_escape_node=False)
    res = build_name(root_node=root_node, method_ls=method_ls, node_ls=node_ls, b_escape_node=False)
    check_consistency(x, res)
