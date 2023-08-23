import optuna
import kevin_toolbox.nested_dict_list as ndl


def sample_from_feasible_domain(var, trial: optuna.trial.BaseTrial, pre_name=""):
    """
        使用试验 trial 基于输入中的定义域 feasible_domain 部分进行参数采样和替换。
            遍历输入中的所有元素，找出符合 <feasible_domain> 格式要求的记录了参数定义域的元素，
            然后使用输入的试验实例 trial 结合参数定义域采样出对应的参数，最后用采样出来的参数替换掉原来的定义域。

        参数：
            inputs:             <list/dict> 当其中的元素满足 <feasible_domain> 格式要求，将进行采样与替换。
                                    <feasible_domain> 格式要求：
                                        1. 是一个 dictionary
                                        2. 包含 "p_type"  字段
                                            "p_type" 表示定义域类型，常见值包括："float" "int" "categorical" 等
                                        3. 根据不同的定义域类型，给出定义域的参数 
                                            比如，p_type="categorical" 时应该包含可选值列表 "choices"
                                            p_type="float"或者"int" 时应该包含最大、最小、间隔值、坐标轴类型 "high" "low" "step" "log" 等
                                        更多参见 https://optuna.readthedocs.io/zh_CN/latest/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial
                                        中的 suggest_xxx() 函数。
            trial:              <optuna.trial.BaseTrial> 试验
            pre_name:           <string> 采样出的参数在试验 trial 中注册的名称的前缀

        返回：
            var, name_ls
                var 是采样后的结果
                name_ls 是被采样的节点名称，注意并不带 pre_name 前缀

        实例：
            对于输入 inputs={
                            "thr":[
                                "interval_thr": {
                                    "p_type": "categorical",
                                    "choices": [
                                      1000,
                                      2000,
                                      5000,
                                      10000
                                    ]
                                },
                                "iou_thr": {
                                    "p_type": "float",
                                    "low": 0,
                                    "high": 1.0000001,
                                    "step": 0.05
                                },
                                "connection": {
                                    "p_type": "categorical",
                                    "choices": {
                                        "skip": lambda x:x,
                                        "and":  lambda x,y : x and y,
                                        "or":  lambda x,y : x or y,
                                    }
                                },
                            ]
                        }
            可能返回的采样结果是 res={"thr":[{"interval_thr":1000}, {"iou_thr":0.6}, {"connection":lambda x:x} ], }。
            当 pre_name="my" 时，这些参数在 trial 中注册的名称分别是 "my:thr@0:interval_thr"，"my:thr@1:iou_thr" 和 "my:thr@1:connection"。
            特别地，
                - 对于字典形式的 choices，其中保存在 trial 中的取值是其键 key 而非 value。
                - 对于list形式，但含有非支持类型的  choices，其中保存在 trial 中的取值是元素的 index。
            这些名称的含义详见 get_value()。
    """

    name_ls=[]

    def func(idx, v):
        nonlocal name_ls
        p_type = v.pop("p_type")
        kwargs = v
        choice_values = None
        if p_type == "categorical":
            # optuna 目前的类别元素仅支持 None, bool, int, float 和 str 类型
            #   对于其他类型的元素，比如 list 和 dict，需要替换成对应 index_ls 或者 key_ls
            #   然后再根据建议的 index 或者 key 到 list 和 dict 中取值
            assert "choices" in kwargs
            if isinstance(kwargs["choices"], (list, tuple,)) and \
                    not all([isinstance(i, (bool, int, float, str,)) or i is None for i in kwargs["choices"]]):
                choice_values = kwargs["choices"]
                kwargs["choices"] = list(range(len(kwargs["choices"])))
            elif isinstance(kwargs["choices"], (dict,)):
                choice_values = kwargs["choices"]
                kwargs["choices"] = list(kwargs["choices"].keys())

        v = eval(f'trial.suggest_{p_type}(name=name, **kwargs)',
                 {"trial": trial, "name": f'{pre_name}{idx}', "kwargs": kwargs})
        if choice_values is not None:
            v = choice_values[v]
        name_ls.append(idx)
        return v

    var = ndl.traverse(var=var, match_cond=lambda _, __, v: isinstance(v, (dict,)) and "p_type" in v,
                       action_mode="replace", converter=func, b_use_name_as_idx=True)

    return var, name_ls
