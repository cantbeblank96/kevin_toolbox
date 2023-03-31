import numpy as np

func = lambda x: 1 / 2 ** 0.5 * np.cos(x * np.pi / 8)

trans_matrix = np.array(
    [
        [0.5, 0.5, 0.5, 0.5],
        [func(1), func(3), -func(3), -func(1)],
        [0.5, -0.5, -0.5, 0.5],
        [func(3), -func(1), func(1), -func(3)]
    ]
).T

shape = list(trans_matrix.shape)
