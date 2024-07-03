import re
from typing import Union
from kevin_toolbox.data_flow.file.markdown.variable import Table_Format


def parse_table(raw_table, output_format: Union[Table_Format, str] = Table_Format.COMPLETE_DICT, orientation="vertical",
                chunk_size=None, chunk_nums=None, b_remove_empty_lines=False, f_gen_order_of_values=None):
    """
        将二维数组形式的表格（比如find_tables()的返回列表的元素），解析成指定的格式

        参数：
            raw_table:                  <list of list> 二维数组形式的表格
            output_format:              <Table_Format or str> 目标格式
                                            具体可以参考 Table_Format 的介绍
            orientation:                <str> 解释表格时取哪个方向
                                            支持以下值：
                                            "vertical" / "v":       将第一行作为标题
                                            "horizontal" / "h":     将第一列作为标题
            chunk_nums:                 <int> 表格被平均分割为多少份进行并列显示。
            chunk_size:                 <int> 表格被按照最大长度进行分割，然后并列显示。
                以上两个参数是用于解释 generate_table() 中使用对应参数生成的表格，其中 chunk_size 仅作检验行数是否符合要求，
                对解释表格无作用。但是当指定该参数时，将视为表格有可能是多个表格并列的情况，因此将尝试根据标题的重复规律，
                推断出对应的 chunk_nums，并最终将其拆分成多个表格。
            b_remove_empty_lines:       <boolean> 移除空的行、列
            f_gen_order_of_values:      <callable> 生成values排序顺序的函数
                                            具体参考 generate_table() 中的对应参数
    """
    assert isinstance(raw_table, (list, tuple,))

    # 转换为字典形式
    if orientation not in ["vertical", "v"]:
        # 需要转为垂直方向
        raw_table = list(zip(*raw_table))
    r_nums, c_nums = len(raw_table), len(raw_table[0])
    if chunk_size is not None:
        assert chunk_size == r_nums - 1, \
            (f'The number of values {r_nums - 1} actually contained in the table '
             f'does not match the specified chunk_size {chunk_size}')
        chunk_nums = c_nums // _find_shortest_repeating_pattern_size(arr=raw_table[0])
    chunk_nums = 1 if chunk_nums is None else chunk_nums
    assert c_nums % chunk_nums == 0, \
        f'The number of headers actually contained in the table does not match the specified chunk_nums, ' \
        f'Expected n*{chunk_nums}, but got {c_nums}'
    # 解释出标题
    keys = raw_table[0][0:c_nums // chunk_nums]
    # 解释出值
    if chunk_nums == 1:
        values = raw_table[1:]
    else:
        values = []
        for i in range(chunk_nums):
            for j in range(1, r_nums):
                values.append(raw_table[j][i * len(keys):(i + 1) * len(keys)])
    # 去除空行
    if b_remove_empty_lines:
        values = [line for line in values if any(i != '' for i in line)]
    table_s = {i: {"title": k, "values": list(v)} for i, (k, v) in enumerate(zip(keys, list(zip(*values))))}
    # 去除空列
    if b_remove_empty_lines:
        table_s = {k: v_s for k, v_s in table_s.items() if v_s["title"] != '' and any(i != '' for i in v_s["values"])}
    # 对值进行排序
    if callable(f_gen_order_of_values):
        breakpoint()
        # 检查是否有重复的 title
        temp = [v["title"] for v in table_s.values()]
        assert len(set(temp)) == len(temp), \
            f'table has duplicate titles, thus cannot be sorted using f_gen_order_of_values'
        idx_ls = list(range(len(values)))
        idx_ls.sort(key=lambda x: f_gen_order_of_values({v["title"]: v["values"][x] for v in table_s.values()}))
        for v in table_s.values():
            v["values"] = [v["values"][i] for i in idx_ls]

    #
    if output_format is Table_Format.SIMPLE_DICT:
        temp = {v_s["title"] for v_s in table_s.values()}
        if len(temp) != len(set(temp)):
            raise AssertionError(
                f'There are columns with the same title in the table, '
                f'please check the orientation of the table or use output_format="complete_dict"')
        table_s = {v_s["title"]: v_s["values"] for v_s in table_s.values()}

    return table_s


def _find_shortest_repeating_pattern_size(arr):
    n = len(arr)

    # 部分匹配表
    pi = [0] * n
    k = 0
    for i in range(1, n):
        if k > 0 and arr[k] != arr[i]:
            k = 0
        if arr[k] == arr[i]:
            k += 1
        pi[i] = k

    # 最短重复模式的长度
    pattern_length = n - pi[n - 1]
    # 是否是完整的重复模式
    if n % pattern_length != 0:
        pattern_length = n
    return pattern_length


if __name__ == '__main__':
    from kevin_toolbox.data_flow.file.markdown import find_tables
    # # 示例Markdown表格文本
    # file_path = ""
    # with open(file_path, 'r') as f:
    #     markdown_text = f.read()

    # markdown_text = """
    # | Name | Age | Occupation |
    # |------|-----|------------|
    # | Alice | 28  | Engineer   |
    # | Bob   | 23  | Teacher    |
    # | Name | Age | Occupation |
    # | Carol | 32  | Hacker   |
    # | David | 18  | Student   |
    # """

    markdown_text = """
|  | a | b |  | a | b |  | a | b |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | 0 | 2 |  | 4 | 6 |  | 7 | 9 |
|  | 1 | 3 |  | 5 | 7 |  | 8 | : |
|  | 2 | 4 |  | 6 | 8 |  | 9 | ; |
|  | 3 | 5 |  |  |  |  |  |  |
"""
    table_ls = find_tables(text=markdown_text)

    # 调用函数并打印结果
    tables = parse_table(raw_table=table_ls[0], output_format="complete_dict", chunk_nums=3, b_remove_empty_lines=True)
    print(tables)
