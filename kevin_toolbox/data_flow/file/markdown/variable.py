from enum import Enum


class Table_Format(Enum):
    """
        表格的几种模式
            1.simple_dict 简易字典模式：
                content_s = {<title>: <list of value>, ...}
                此时键作为标题，值作为标题下的一系列值。
                由于字典的无序性，此时标题的顺序是不能保证的，若要额外指定顺序，请使用下面的 完整模式。
            2. complete_dict 完整字典模式:
                content_s = {<index>: {"title": <title>,"values":<list of value>}, ...}
                此时将取第 <index> 个 "title" 的值来作为第 <index> 个标题的值。values 同理。
                该模式允许缺省某些 <index>，此时这些 <index> 对应的行/列将全部置空。
    """
    SIMPLE_DICT = "simple_dict"
    COMPLETE_DICT = "complete_dict"
