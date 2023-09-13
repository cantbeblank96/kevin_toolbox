import copy
import kevin_toolbox.nested_dict_list as ndl
import torch


def copy_(var, b_deepcopy=False):
    """
        复制嵌套字典列表 var，并返回其副本

        参数：
            var
            b_deepcopy:         <boolean> 是否进行深拷贝
                                    默认为 False 此时仅复制结构，但叶节点仍在 var 和其副本之间共享
                                    当设置为 True 时，进行完全的深拷贝
    """
    if b_deepcopy:
        try:
            res = copy.deepcopy(var)
        except:
            res = _copy_structure(var=var)
            res = _copy_nodes(var=res)
    else:
        res = _copy_structure(var=var)

    return res


def _copy_structure(var):
    """
        复制结构
            只复制 ndl 中的 dict、list 结构，复制前后 ndl 中的叶节点（亦即dict、list中的元素仍然保持共享）
    """
    return ndl.traverse(var=[var], match_cond=lambda _, __, value: isinstance(value, (list, dict,)),
                        action_mode="replace", converter=lambda _, value: value.copy(),
                        traversal_mode="dfs_pre_order", b_traverse_matched_element=True)[0]


def _copy_nodes(var):
    """
        复制叶节点
            复制并替换 ndl 中的叶节点
    """

    def func(_, value):
        if torch.is_tensor(value):
            return value.detach().clone()
        else:
            return copy.deepcopy(value)

    return ndl.traverse(var=[var], match_cond=lambda _, __, value: not isinstance(value, (list, dict,)),
                        action_mode="replace", converter=func,
                        traversal_mode="dfs_pre_order", b_traverse_matched_element=True)[0]


if __name__ == '__main__':
    x = dict(acc=[0.66, 0.78, 0.99], )
    copy_(var=x, b_deepcopy=False)
