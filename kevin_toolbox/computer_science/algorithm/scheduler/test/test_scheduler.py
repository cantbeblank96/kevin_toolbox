import pytest
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.computer_science.algorithm.scheduler import Trigger, Strategy_Manager


def test_Trigger():
    print("test scheduler.Trigger()")

    res_ls = []

    def func_(x):
        nonlocal res_ls
        res_ls.append(x)

    class cls_:
        @staticmethod
        def update_by_state(x):
            nonlocal res_ls
            res_ls.append(x)

    tg = Trigger()
    # 绑定单个函数
    tg.bind_func(target=func_)
    tg.update_by_state(cur_state=dict(epoch=1))
    check_consistency(res_ls, [{'epoch': 1}])
    tg.update_by_state(cur_state=dict(epoch=1))
    check_consistency(res_ls, [{'epoch': 1}])  # 状态没有更新，不调用绑定的函数

    res_ls.clear()
    # 绑定多个函数/对象
    tg.bind(target=[func_, cls_()])
    tg.update_by_state(cur_state=dict(epoch=2))
    check_consistency(res_ls, [{'epoch': 2}] * 3)  # 状态没有更新，不调用绑定的函数
    tg.update_by_state(cur_state=dict(epoch=2))
    check_consistency(res_ls, [{'epoch': 2}] * 3)


def test_Strategy_Manager():
    print("test scheduler.Strategy_Manager()")

    sm = Strategy_Manager(strategy={
        "__dict_form": "para_name:trigger_value",
        "__trigger_name": "epoch",
        ":lr": {
            "<f>lambda t: t%100==0": "<f>lambda p, t: round(p*0.1,4)",
        },
        ":weight_decay:beta": {
            "<f>lambda t: t%300==0": "<f>lambda p, t: t",
        },
    })
    sm.add(strategy={
        "__dict_form": "trigger_value:para_name",
        "__trigger_name": "step",
        0: {
            ":lr": 0.1,
            ":ratio_ls": [1e-3, 1e-2],
            ":weight_decay": {"beta": 0, "alpha": 0},
        },
        300: {
            ":ratio_ls@1": 1e-5,
        },
        200: {
            ":weight_decay:alpha": 1,
        },
        "<f>lambda t: t%100==0": {
            ":weight_decay:alpha": "<f>lambda p, t: p+1",
        },
    }, override=False)

    var, action_s = sm.cal(trigger_state=dict(step=0, ), var=dict())
    check_consistency(var, {
        "lr": 0.1,
        "ratio_ls": [1e-3, 1e-2],
        "weight_decay": {"beta": 0, "alpha": 1},
    })
    check_consistency(action_s, {
        'step': [
            (':lr', 0.1),
            (':ratio_ls', [0.001, 0.01]),
            (':weight_decay', {'beta': 0, 'alpha': 0}),
            (':weight_decay:alpha', '<f>lambda p, t: p+1')
        ]
    })

    var_1, action_s_1 = sm.cal(trigger_state=dict(step=50, ), var=var)
    check_consistency(var, var_1)
    check_consistency(action_s_1, {'step': []})

    var_2, action_s_2 = sm.cal(trigger_state=dict(step=100, ), var=var_1)
    check_consistency(var_2["weight_decay"], {"beta": 0, "alpha": 2})
    check_consistency(action_s_2, {'step': [(':weight_decay:alpha', '<f>lambda p, t: p+1')]})

    # 验证当 para_name 相同时，值匹配比函数匹配更加优先
    var_3, action_s_3 = sm.cal(trigger_state=dict(step=200, ), var=var_2)
    check_consistency(var_3["weight_decay"], {"beta": 0, "alpha": 1})
    check_consistency(action_s_3, {'step': [(":weight_decay:alpha", 1)]})

    # 验证当 para_name 相同时，值匹配比函数匹配更加优先
    var_4, action_s_4 = sm.cal(trigger_state=dict(epoch=300, step=300, ), var=var_3)
    check_consistency(var_4, {
        "lr": 0.01,
        "ratio_ls": [1e-3, 1e-5],
        "weight_decay": {"beta": 300, "alpha": 2},
    })
    check_consistency(action_s_4, {
        'step': [(":ratio_ls@1", 1e-5),
                 (":weight_decay:alpha", "<f>lambda p, t: p+1")],
        "epoch": [(":lr", "<f>lambda p, t: round(p*0.1,4)"),
                  (":weight_decay:beta", "<f>lambda p, t: t")]
    })
