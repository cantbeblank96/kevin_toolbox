## 简介

本模块中算法主要面向 nested dictionary-list 类型数据。



## 数据结构



#### nested dictionary-list 嵌套字典列表

嵌套字典列表（nested dictionary-list）是由Python中的字典类型和列表类型组成的复杂数据结构，它可以用于表示具有层次结构的数据。在嵌套字典列表中，一个字典中的值/列表中的值可以是另外一个字典、列表或其他数据类型，这些嵌套的数据类型也可以再次包含字典和列表等其他类型的数据。

例如，下面是一个简单的嵌套字典列表：

```json
{
   "person1": {
        "name": "Alice",
        "age": 28,
        "hobbies": ["reading", "swimming"]
    },
   "person2": {
        "name": "Bob",
        "age": 35,
        "hobbies": ["hiking", "photography"]
    }
}
```

 

#### name 名字

名字（name）对应于嵌套字典列表中的一个位置。它由 "<变量名>" 加上多组 "<取值方式><键>" 组成。

```
<变量名>
    在实际使用时，比如 get_value()等函数，一般忽略该部分。
<取值方式>
    支持以下几种:
        "@"     表示使用 eval() 读取键
        ":"     表示使用 str() 读取键
        "|"     表示依次尝试 str() 和 eval() 两种方式
    示例:
        "@100"      表示读取 var[eval("100")]
        ":epoch"    表示读取 var["epoch"]
        "|1+1"    表示首先尝试读取 var["1+1"]，若不成功则尝试读取 var[eval("1+1")]
<键>
    对于含有特殊字符 :|@ 的 key，应该先对 key 中的这些特殊字符使用 \ 进行转义
        比如，对于：
            var={"acc@epoch=1": 0.05, "acc@epoch=2": 0.06}
        在 var["acc@epoch=1"] 位置上的元素的名字可以是
            "var:acc\@epoch=1"
```

