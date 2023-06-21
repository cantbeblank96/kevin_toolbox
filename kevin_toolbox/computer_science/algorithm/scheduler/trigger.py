class Trigger:
    """
        触发器
            通过 self.update_by_state() 来接收并监视 state_dict，
            当 state_dict 全部或部分发生变化时，将会把【发生变化的部分】
            传入 self.bind() 绑定的函数中，并执行一次该函数。
    """

    def __init__(self, **kwargs):
        """
            参数：
                target:             <func or obj/list of func or obj> 待绑定目标
                                        默认为空
                init_state          <dict> 初始状态
                                        默认不设置，此时将在第一次调用 self.update_by_state() 时设置
        """
        # 默认参数
        paras = {
            #
            "target": [],
            "init_state": dict()
        }

        # 获取参数
        paras.update(kwargs)

        self.last_state = paras["init_state"]
        self.func_ls = []
        self.bind_func(target=paras["target"])

    def bind_func(self, target):
        """
            绑定函数

            参数：
                target:     <func/list of func>
        """
        target = [target] if not isinstance(target, (list, tuple,)) else target
        for func in target:
            assert callable(func)
        self.func_ls.extend(target)

    def bind_obj(self, target):
        """
            绑定实例
                要求实例具有 update_by_state() 方法

            参数：
                target:     <func/list of obj>
        """
        target = [target] if not isinstance(target, (list, tuple,)) else target
        temp = []
        for i in target:
            func = getattr(i, "update_by_state", None)
            assert callable(func), \
                f'there is no update_by_state() method in the object {i} to be bound'
            temp.append(func)
        self.func_ls.extend(temp)

    def bind(self, target):
        """
            依次尝试通过 bind_func() 和 bind_obj() 方法对 target 进行绑定
        """
        target = [target] if not isinstance(target, (list, tuple,)) else target
        for i in target:
            try:
                self.bind_func(target=i)
            except:
                self.bind_obj(target=i)

    def update_by_state(self, cur_state):
        """
            更新状态，决定是否触发
        """
        assert isinstance(cur_state, (dict,))

        new_state = dict()
        for key, value in cur_state.items():
            if key not in self.last_state or self.last_state[key] != value:
                new_state[key] = value

        if len(new_state) > 0:
            for func in self.func_ls:
                func(new_state)
            self.last_state.update(new_state)

        return new_state
