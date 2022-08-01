def get_inverse_of_transpose_index_ls(index_ls):
    """
        获取转置的逆
            对于任意 index_ls，有：
                x.transpose(*index_ls).transpose(*reverse_index_ls(index_ls)) == x
            恒成立。

        参数：
            index_ls:   <list> 格式具体参考 dimension.coordinates
    """

    pairs = [[r_i, i] for r_i, i in enumerate(index_ls)]
    pairs.sort(key=lambda x: x[-1])
    r_index_ls = [i[0] for i in pairs]
    return r_index_ls
