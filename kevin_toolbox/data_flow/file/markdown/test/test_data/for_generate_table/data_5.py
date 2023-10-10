from collections import OrderedDict

content_s = OrderedDict({
    "y/n": [True] * 5 + [False] * 5,
    "a": list(range(10)),
    "b": [chr(i) for i in range(50, 60, 2)]
})
param_s = dict(orientation="v", chunk_size=4, b_allow_misaligned_values=True,
               f_gen_order_of_values=lambda x: (-int(x["y/n"] is False), -(x["a"] % 3)))
