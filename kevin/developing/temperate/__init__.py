"""
iterable、iterator、sequence、generator之间的差别
（整理自：https://zhuanlan.zhihu.com/p/403830796）
Iterable（可迭代对象）
    实现 __iter()__ 或 __getitem()__ 方法
Sequence（序列）/Map（映射）
    实现 __getitem()__ 和 __len__() 方法
Iterator（迭代器）
    实现 __iter__() 和 __next__() 方法
generator（生成器）
    含有yield的函数，或者使用生成器推导式生成的生成器
"""
