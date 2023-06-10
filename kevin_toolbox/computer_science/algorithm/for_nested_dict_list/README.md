嵌套字典列表（nested dictionary-list）是由Python中的字典类型和列表类型组成的复杂数据结构，它可以用于表示具有层次结构的数据。在嵌套字典列表中，一个字典中的值/列表中的值可以是另外一个字典、列表或其他数据类型，这些嵌套的数据类型也可以再次包含字典和列表等其他类型的数据。

例如，下面是一个简单的嵌套字典列表：

```
python复制代码{
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

本模块中算法主要面向 nested dictionary-list 类型数据。 
