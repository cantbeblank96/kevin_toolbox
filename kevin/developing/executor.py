class Executor:
    """
        执行器
            允许以静态方式描述并保存一个执行过程，
            然后在你需要的地方再进行调用。

        用法：
            1.定义执行过程
                get_executor_ls = Executor()
                get_executor_ls.set_config( func = <function>,
                                            args = <list/tuple>,
                                            kwargs = <dict>,
                                            f_args = <list of functions>,
                                            f_kwargs = <dict of (key, function) pairs>)
                # 其中 func 是执行过程的主体函数
                # args 和 kwargs 是运行该函数时，要输入的参数
                # f_args 和 f_kwargs 的前缀 f_ 是 fixtures 固件的缩写
                #     固件内包含一系列的函数
                #     这些函数会在 func 执行前被首先执行，然后将得到的结果更新到参数中
                #     对于 f_args，执行后的结果会被 append 到 args 后面
                #     对于 f_kwargs，其中的 value 被执行后的结果将替换原来的 value，然后 update 到 kwargs 中
                # 使用 fixtures 的一大优势，就是可以让一些参数可以等到函数需要执行前再生成，从而节约资源
            2.调用执行过程
                get_executor_ls.run()
                # 等效于 get_executor_ls()

        注意！！
            对于 fixtures 中的函数，在定义函数时，函数体中如果涉及有外部的变量，
            则务必注意这些外部变量可能被修改，从而引起函数的行为发生不可预期的变化，
            例如：
                >> k=2
                >> y=lambda x:x**int(k)
                >> y(2)
                # 4
                >> k=4
                >> y(2)
                # 16
            解决方法：
                使用 Executor 来构造 fixtures 中的函数，同时使用 deepcopy 对参数进行隔离。
    """

    def __init__(self, *args, **kwargs):
        self.config = dict()
        self.set_config(*args, **kwargs)

    def set_config(self, func, **paras):
        """
            定义执行过程
        """
        config = dict()

        # func
        assert callable(func), \
            TypeError(f"func should be callable, but get a {type(func)}")
        config["func"] = func

        # args
        args = paras.get("args", None)
        if args is not None:
            assert isinstance(args, (list, tuple,))
            config["args"] = list(args)
        # kwargs
        kwargs = paras.get("kwargs", None)
        if kwargs is not None:
            assert isinstance(kwargs, (dict,))
            config["kwargs"] = kwargs

        # f_args
        f_args = paras.get("f_args", None)
        if f_args is not None:
            assert isinstance(f_args, (list, tuple,))
            for f in f_args:
                assert callable(f)
            config["f_args"] = list(f_args)
        # f_kwargs
        f_kwargs = paras.get("f_kwargs", None)
        if f_kwargs is not None:
            assert isinstance(f_kwargs, (dict,))
            for k, v in f_kwargs.items():
                assert callable(v) and isinstance(k, (str,))
            config["f_kwargs"] = f_kwargs

        # update config
        self.config.update(config)

    def run(self):
        """
            调用执行过程
        """
        assert "func" in self.config, \
            Exception(f"you should use set_config() to set config, before calling run()")

        # 获取函数
        func = self.config["func"]

        # 获取参数
        args, kwargs = [], dict()
        if "args" in self.config:
            args.extend(self.config["args"])
        if "kwargs" in self.config:
            kwargs.update(self.config["kwargs"])

        # evaluate the fixtures
        if "f_args" in self.config:
            for f in self.config["f_args"]:
                args.append(f())
        if "f_kwargs" in self.config:
            for k, v in self.config["f_kwargs"].items():
                kwargs[k] = v()

        # 执行
        return func(*args, **kwargs)

    def __call__(self):
        return self.run()


if __name__ == '__main__':
    #
    executor = Executor(func=lambda x, y: print(x + y), args=[1], kwargs={"y": 3})
    print("get_executor_ls")
    executor()
    #
    executor = Executor(func=lambda x, y: print(x, y), f_args=[lambda: 3], f_kwargs={"y": lambda: 4})
    print("get_executor_ls using fixtures")
    executor()