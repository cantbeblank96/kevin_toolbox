from kevin_toolbox.computer_science.algorithm.for_nested_dict_list import set_value_by_name, get_value_by_name


def eval_references(var, node_s, order, converter=None):
    """
        将 var 中的具有引用的值替换为计算结果

        参数：
            var:
            node_s:             <dict> 引用节点，parse_references() 返回的结果
            order:              <list of name> 计算顺序，cal_relation_between_references() 返回的结果
            converter:          <callable> 对计算结果施加何种处理
    """
    assert order is not None and set(order).issubset(set(node_s.keys()))
    assert converter is None or callable(converter)

    for name in order:
        details = node_s[name]
        # 获取依赖值
        for k, v in details["paras"].items():
            v_new = get_value_by_name(var=var, name=v)
            if converter is not None:
                v_new = converter(v_new)
            details["paras"][k] = v_new
        # 计算
        res = eval(details["expression"], details["paras"])
        # 赋值
        set_value_by_name(var=var, name=name, value=res, b_force=False)
