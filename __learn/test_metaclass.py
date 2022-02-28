class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        print(cls, name, bases, attrs)
        res = type(name, bases, attrs)
        print(res)
        return res


class MyModel(metaclass=ModelMetaclass):
    here = 233

    def __init__(self):
        self.var = {1: 2}
        print(self.var)


if __name__ == '__main__':
    myModel = MyModel()
    """
    <class '__main__.ModelMetaclass'> MyModel () {'__module__': '__main__', '__qualname__': 'MyModel', 'here': 233, '__init__': <function MyModel.__init__ at 0x7f13fc90aef0>}
    <class '__main__.MyModel'>
    {1: 2}
    """
    # metaclass 定义了生成类的方式，而 ModelMetaclass 中获取的 name, bases, attrs 是关于类的名称，父类和类属性，注意这里的属性是类型，不包含实例属性
