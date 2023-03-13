import copy
import torch
import numpy as np


class Exponential_Moving_Average:
    def __init__(self, **kwargs):
        """
            滑动平均计数器
                支持为每个输入数据配置不同的权重
                参考： https://www.cnblogs.com/wuliytTaotao/p/9479958.html

            参数：
                keep_ratio:             <float> 对历史值的保留比例。
                                            其意义为： 大致等于计算过去 1/keep_ratio 个数据的平均值
                                            默认为 0.99
                                            当设置为 0 时相当于仅保留最新的数据
                bias_correction:        <boolean> 是否开启偏差修正。
                                            默认为 True
                指定输入数据的格式，有三种方式：
                    1. 显式指定数据的形状和所在设备等。
                        data_format:        <dict of paras>
                                其中需要包含以下参数：
                                    type_:              <str>
                                                            "numpy":        np.ndarray
                                                            "torch":        torch.tensor
                                    shape:              <list of integers>
                                    device:             <torch.device>
                                    dtype:              <torch.dtype>
                    2. 根据输入的数据，来推断出形状、设备等。
                        like:               <torch.tensor / np.ndarray>
                    3. 均不指定 data_format 和 like，此时将等到第一次调用 add_element()/add_sequence() 时再根据输入来自动推断。
                    以上三种方式，默认选用最后一种。
                    如果三种方式同时被指定，则优先级与对应方式在上面的排名相同。
        """

        # 默认参数
        paras = {
            # 超参数
            "keep_ratio": 0.99,
            "bias_correction": True,
            # 指定 tensor 的形状、设备
            "data_format": None,
            #
            "like": None,
        }

        # 获取参数
        paras.update(kwargs)

        # 校验参数
        assert isinstance(paras["keep_ratio"], (int, float,)) and 0 <= paras["keep_ratio"] <= 1
        #
        self.paras = paras
        self.value = self._init_value(like=paras["like"], data_format=paras["data_format"])
        self.state = dict(
            total_nums=0,
            bias_fix=1,
        )

    @staticmethod
    def _init_value(like=None, data_format=None):
        if like is not None:
            if torch.is_tensor(like):
                value = torch.zeros_like(like)
            elif isinstance(like, (np.ndarray,)):
                value = np.zeros_like(like)
            else:
                raise ValueError("paras 'like' should be np.ndarray or torch.tensor")
        elif data_format is not None:
            assert isinstance(data_format, (dict,)) and "type_" in data_format and "shape" in data_format
            k_s = copy.deepcopy(data_format)
            k_s.pop("type_")
            k_s.pop("shape")
            if data_format["type_"] == "torch":
                value = torch.zeros(size=data_format["shape"], **k_s)
            else:
                value = np.zeros(shape=data_format["shape"], **k_s)
        else:
            value = None

        return value

    def add_sequence(self, item_ls, weight_ls=None):
        if weight_ls is not None:
            if isinstance(weight_ls, (int, float,)):
                weight_ls = [weight_ls] * len(item_ls)
            assert len(weight_ls) == len(item_ls)
            for item, weight in enumerate(item_ls, weight_ls):
                self.add_element(item, weight)
        else:
            for item in item_ls:
                self.add_element(item)

    def add_element(self, item, weight=1):
        if self.value is None:
            self.value = self._init_value(like=item)
        new_ratio = (1 - self.paras["keep_ratio"]) * weight
        keep_ratio = (1 - new_ratio)
        self.value = keep_ratio * self.value + new_ratio * item
        #
        self.state["total_nums"] += 1
        self.state["bias_fix"] *= keep_ratio

    def get_value(self, bias_correction=None):
        assert self.value is not None, \
            f'Lack of initial value, pls invoke add_element()/add_sequence() first'
        bias_correction = self.paras["bias_correction"] if bias_correction is None else bias_correction
        if bias_correction:
            return self.value / (1 - self.state["bias_fix"] + 1e-10)
        else:
            return self.value

    def clear(self):
        if self.value is not None:
            self.value[:] = 0
        self.state = dict(
            total_nums=0,
            bias_fix=1,
        )


if __name__ == '__main__':
    seq = list(torch.tensor(range(1, 10)))
    ema = Exponential_Moving_Average(keep_ratio=0.9, bias_correction=True)
    for i, item in enumerate(seq):
        ema.add_element(item=item)
        print(i, item, ema.get_value(), ema.state["bias_fix"])
