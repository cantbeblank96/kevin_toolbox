import torch
import numpy as np

inputs_ls = []
outputs_raw_ls = []
outputs_unbiased_ls = []

"""
该测试数据来源：
    https://www.cnblogs.com/wuliytTaotao/p/9479958.html
"""
inputs = [10, 20, 10, 0, 10, 20, 30, 5, 0, 10, 20, 10, 0, 10, 20, 30, 5, 0, 10, 20, 10, 0, 10, 20, 30, 5, 0, 10, 20,
          10, 0, 10, 20, 30, 5]
outputs_raw = [1.0, 2.9, 3.61, 3.249, 3.9241, 5.5317, 7.9785, 7.6807, 6.9126, 7.2213, 8.4992, 8.6493, 7.7844, 8.0059,
               9.2053, 11.2848, 10.6563, 9.5907, 9.6316, 10.6685, 10.6016, 9.5414, 9.5873, 10.6286, 12.5657, 11.8091,
               10.6282, 10.5654, 11.5089, 11.358, 10.2222, 10.2, 11.18, 13.062, 12.2558]
outputs_unbiased = [10.0, 15.2632, 13.321, 9.4475, 9.5824, 11.8057, 15.2932, 13.4859, 11.2844, 11.0872, 12.3861,
                    12.0536, 10.4374, 10.3807, 11.592, 13.8515, 12.7892, 11.2844, 11.1359, 12.145, 11.9041, 10.5837,
                    10.5197, 11.5499, 13.5376, 12.6248, 11.2844, 11.1489, 12.0777, 11.8608, 10.6276, 10.5627, 11.5365,
                    13.4357, 12.5704]
inputs_ls.append(inputs)
outputs_raw_ls.append(outputs_raw)
outputs_unbiased_ls.append(outputs_unbiased)

"""
转换为 torch.tensor
"""
inputs_ls.append([torch.as_tensor([i] * 4) for i in inputs])
outputs_raw_ls.append([torch.as_tensor([i] * 4) for i in outputs_raw])
outputs_unbiased_ls.append([torch.as_tensor([i] * 4) for i in outputs_unbiased])

"""
转换为 np.array
"""
inputs_ls.append([np.asarray([i] * 4) for i in inputs])
outputs_raw_ls.append([np.asarray([i] * 4) for i in outputs_raw])
outputs_unbiased_ls.append([np.asarray([i] * 4) for i in outputs_unbiased])
