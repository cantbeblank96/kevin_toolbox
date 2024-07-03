import re


def find_tables(text):
    """
        查找文本中的表格
            将返回一个列表，列表每个元素系一个二维的数组，表示一个原始的表格
    """
    table_ls = []
    for sub_text in text.split('\n\n', -1):
        ret = _find_table(text=sub_text)
        if ret is not None:
            table_ls.append(ret)

    return table_ls


def _find_table(text):
    # 正则表达式匹配Markdown表格
    table_pattern = re.compile(r'\|([^\n]+)\|', re.DOTALL)
    table_matches = table_pattern.findall(text)
    if len(table_matches) < 2:
        # 因为一个合法的 markdown 表格需要含有表头的分隔线，所以行数至少应该为 2
        return None

    # 去除表头的分隔线
    table_matches.pop(1)
    #
    tables = []  # 每个元素为一行
    for match in table_matches:
        # 分割每一行
        tables.append([i.strip() for i in match.split('|', -1)])

    return tables


if __name__ == '__main__':
    # # 示例Markdown表格文本
    # file_path = ""
    # with open(file_path, 'r') as f:
    #     markdown_text = f.read()

    markdown_text = """
| Name | Age | Occupation |
|------|-----|------------|
| Alice | 28  | Engineer   |
| Bob   | 23  | Teacher    |
| Name | Age | Occupation |
| Carol | 32  | Hacker   |
| David | 18  | Student   |

2333

|  | a | b |  | a | b |  | a | b |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | 0 | 2 |  | 4 | 6 |  | 7 | 9 |
|  | 1 | 3 |  | 5 | 7 |  | 8 | : |
|  | 2 | 4 |  | 6 | 8 |  | 9 | ; |
|  | 3 | 5 |  |  |  |  |  |  |
"""

    # 调用函数并打印结果
    tables = find_tables(text=markdown_text)
    print(tables[0])
    print(tables[1])
