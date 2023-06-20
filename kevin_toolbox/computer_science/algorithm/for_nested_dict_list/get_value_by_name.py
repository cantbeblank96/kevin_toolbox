from kevin_toolbox.computer_science.algorithm.for_nested_dict_list.name_handler import parse_name


def get_value_by_name(var, name):
    """
        通过解释名字得到取值方式，然后到 var 中获取对应部分的值。

        参数：
            var:            任意支持索引取值的变量
            name:           <str> 名字
                                名字 name 的具体介绍参见函数 name_handler.parse_name()
                                假设 var=dict(acc=[0.66,0.78,0.99])，如果你想读取 var["acc"][1] => 0.78，那么可以将 name 写成：
                                    ":acc@1" 或者 "|acc|1" 等。
                                注意，在 name 的开头也可以添加任意非解释方式的字符，本函数将直接忽略它们，比如下面的:
                                    "var:acc@1" 和 "xxxx|acc|1" 也能正常读取。
    """
    _, method_ls, node_ls = parse_name(name=name, b_de_escape_node=True)

    for method, node in zip(method_ls, node_ls):
        if method == "@":
            var = var[eval(node)]
        elif method == "|":
            try:
                var = var[node]
            except:
                var = var[eval(node)]
        else:  # ":"
            var = var[node]

    return var
