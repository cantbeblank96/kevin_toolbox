import pytest
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.computer_science.algorithm.scheduler import Trigger, Strategy_Manager


def test_Trigger():
    print("test scheduler.Trigger()")

    res_ls = []

    def func_(x):
        nonlocal res_ls
        res_ls.append(x)

    def func_2(x):
        nonlocal res_ls
        res_ls.append("invoke func_2")

    class cls_:
        @staticmethod
        def update_by_state(x):
            nonlocal res_ls
            res_ls.append("invoke cls_")

    # 绑定
    #   在初始化时绑定
    tg = Trigger(target_s={":func@0": func_}, init_state=dict(epoch=0))
    tg.update_by_state(cur_state=dict(epoch=1))
    check_consistency(res_ls, [{'epoch': 1}])
    tg.update_by_state(cur_state=dict(epoch=1))
    check_consistency(res_ls, [{'epoch': 1}])  # 状态没有更新，不调用绑定的函数
    #   使用 bind() 绑定
    tg.bind(name=":func@1", target=func_2)
    tg.bind(name=":inst@0", target=cls_())
    tg.update_by_state(cur_state=dict(epoch=2), target_names=[":func@1", ":inst@0"])
    check_consistency(res_ls, [{'epoch': 1}, "invoke func_2", "invoke cls_"])
    #   使用 unbind() 解除绑定
    try:
        tg.unbind(name=":func@2", b_not_exist_ok=False)
    except:
        assert True
    else:
        assert False
    tg.unbind(name=":func@1", b_not_exist_ok=False)
    tg.update_by_state(cur_state=dict(epoch=3), target_names=[":func", ":inst"])
    check_consistency(res_ls, [{'epoch': 1}, "invoke func_2", "invoke cls_", {'epoch': 3}, "invoke cls_"])
    res_ls.clear()

    # 保存和加载触发器的状态
    tg_state = tg.state_dict()
    #
    tg.clear_state_dict()
    tg.update_by_state(cur_state=dict(epoch=3), target_names=[":inst", ":func"])
    check_consistency(res_ls, ["invoke cls_", {'epoch': 3}])  # 状态有更新
    res_ls.clear()
    #
    tg.clear_state_dict()
    tg.load_state_dict(tg_state)
    tg.update_by_state(cur_state=dict(epoch=3), target_names=[":inst", ":func"])
    check_consistency(res_ls, [])  # 状态没有更新，不调用绑定的函数


def test_Strategy_Manager():
    print("test scheduler.Strategy_Manager()")

    sm = Strategy_Manager(strategy={
        "__dict_form": "para_name:trigger_value",
        "__trigger_name": "epoch",
        ":lr": {
            "<eval>lambda t: t%100==0": "<eval>lambda p, t: round(p*0.1,4)",
        },
        ":weight_decay:beta": {
            "<eval>lambda t: t%300==0": "<eval>lambda p, t: t",
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
        "<eval>lambda t: t%100==0": {
            ":weight_decay:alpha": "<eval>lambda p, t: p+1",
        },
    }, override=False)

    var, action_s = sm.cal(trigger_state=dict(step=0, ), var=dict())
    check_consistency(var, {
        "lr": 0.1,
        "ratio_ls": [1e-3, 1e-2],
        "weight_decay": {"beta": 0, "alpha": 1},
    })
    assert callable(action_s["step"][-1][1]) and action_s["step"][-1][1](1, 0) == 2
    check_consistency(action_s, {
        "step": [
            (':lr', 0.1),
            (':ratio_ls', [0.001, 0.01]),
            (':weight_decay', {'beta': 0, 'alpha': 0}),
            (':weight_decay:alpha', action_s["step"][-1][1])  # '<eval>lambda p, t: p+1'
        ]
    })

    var_1, action_s_1 = sm.cal(trigger_state=dict(step=50, ), var=var)
    check_consistency(var, var_1)
    check_consistency(action_s_1, {"step": []})

    var_2, action_s_2 = sm.cal(trigger_state=dict(step=100, ), var=var_1)
    check_consistency(var_2["weight_decay"], {"beta": 0, "alpha": 2})
    assert callable(action_s_2["step"][-1][1]) and action_s_2["step"][-1][1](1, 0) == 2
    check_consistency(action_s_2,
                      {"step": [(':weight_decay:alpha', action_s_2["step"][-1][1])]})  # '<eval>lambda p, t: p+1'

    # 验证当 para_name 相同时，值匹配比函数匹配更加优先
    var_3, action_s_3 = sm.cal(trigger_state=dict(step=200, ), var=var_2)
    check_consistency(var_3["weight_decay"], {"beta": 0, "alpha": 1})
    check_consistency(action_s_3, {"step": [(":weight_decay:alpha", 1)]})

    # 验证当 para_name 相同时，值匹配比函数匹配更加优先
    var_4, action_s_4 = sm.cal(trigger_state=dict(epoch=300, step=300, ), var=var_3)
    check_consistency(var_4, {
        "lr": 0.01,
        "ratio_ls": [1e-3, 1e-5],
        "weight_decay": {"beta": 300, "alpha": 2},
    })
    assert callable(action_s_4["step"][-1][1]) and action_s_4["step"][-1][1](1, 0) == 2
    assert callable(action_s_4["epoch"][0][1]) and action_s_4["epoch"][0][1](1, 0) == round(1 * 0.1, 4)
    assert callable(action_s_4["epoch"][1][1]) and action_s_4["epoch"][1][1](1, 0) == 0
    check_consistency(action_s_4, {
        "step": [(":ratio_ls@1", 1e-5),
                 (":weight_decay:alpha", action_s_4["step"][-1][1])],  # "<eval>lambda p, t: p+1"
        "epoch": [(":lr", action_s_4["epoch"][0][1]),  # "<eval>lambda p, t: round(p*0.1,4)"
                  (":weight_decay:beta", action_s_4["epoch"][1][1])]  # "<eval>lambda p, t: t"
    })
