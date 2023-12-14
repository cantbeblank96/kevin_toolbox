from kevin_toolbox.nested_dict_list import get_value, set_value


def set_default(var, name, default, b_force=False, cache_for_verified_names=None):
    """
        当 name 指向的位置在 var 中不存在时，将会把 default 插入到对应的位置。
            （类似于 dict.setdefault() 的行为）

        参数：
            var:            任意支持索引赋值的变量
            name:           <string> 名字（位置）
                                名字 name 的具体介绍参见函数 name_handler.parse_name()
            default:        默认值
            b_force:        <boolean> 当无法将 default 设置到 name 指定的位置时，是否尝试创建或者修改 var 中的节点
                                默认为 False，此时若无法设置，则报错
                                当设置为 True，可能会对 var 的结构产生不可逆的改变，请谨慎使用。
                注意：
                    若 b_force 为 True 有可能不会在 var 的基础上进行改变，而是返回一个新的ndl结构，
                    因此建议使用赋值 var = ndl.set_default(var) 来避免可能的错误。

            cache_for_verified_names:   <set> 用于缓存已检验的 name
                                默认为 None，不使用缓存。
                                当设为某个集合时，将开启缓存。此时将首先判断 name 是否在缓存中，若在，则视为之前已经对该 name 成功进行过 set_default()
                                    操作，没有必要再重复执行，因此直接跳过后续流程；若不在，则执行 set_default() 操作，并在成功执行之后将该 name
                                    补充到缓存中。
                                合理利用该缓存机制将可以避免对同一个 name 反复进行 set_default() 操作，从而提高效率。
    """
    if cache_for_verified_names is not None:
        assert isinstance(cache_for_verified_names, (set,))
        if name in cache_for_verified_names:
            return var

    temp = list()
    if id(temp) == id(get_value(var=var, name=name, default=temp)):
        # 获取失败，说明 name 指向的位置不存在，则尝试创建
        var = set_value(var=var, name=name, value=default, b_force=b_force)

    if cache_for_verified_names is not None:
        cache_for_verified_names.add(name)
    return var
