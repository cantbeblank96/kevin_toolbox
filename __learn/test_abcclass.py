from abc import ABC, abstractmethod


class MyABC(ABC):
    here = 233

    def __init__(self):
        super().__init__()
        self.var = {1: 2}
        print(self.var)

    @abstractmethod
    def func(self):
        print(2333)


class Implement(MyABC):
    def func(self):
        super().func()


if __name__ == '__main__':
    myModel = Implement()
    """
    结论：
        可以先在抽象方法中定义实体，然后在实现类中通过 super().func() 调用，不会报错。
    """
