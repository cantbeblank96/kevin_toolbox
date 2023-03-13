import numpy as np

from kevin.math.dimension import coordinates, reshape
from kevin.patches.for_matplotlib import add_trajectory_2d, add_trajectory_3d

import matplotlib.pyplot as plt
import matplotlib.axes._axes as axes
from mpl_toolkits.mplot3d import Axes3D  # 3d坐标系
import matplotlib.figure as figure

# 支持中文
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# ------------ 准备数据 ------------ #
# points = coordinates.generate(shape=[3, 3, 3], pattern="z_pattern", output_format="indices_ls")
points = coordinates.generate(shape=[4, 4, 4], pattern="shuffle_inside_block", output_format="indices_ls",
                              kwargs=dict(stride=2, kernel_size=2, seed=1145141919))
# points = coordinates.generate(shape=[3, 3, 3], pattern="normal", output_format="indices_ls",
#                               kwargs=dict(order="F"))

# ------------ 准备画布与图层 ------------ #
fig = plt.figure(figsize=(8, 6))  # type:figure.Figure
ax3d = fig.add_subplot(1, 1, 1, projection='3d')  # type:Axes3D

# ------------ 绘制图形元素 ------------ #
add_trajectory_3d(ax3d=ax3d, points=points[:3])

# ------------ 调整元素属性，处理细节 ------------ #

"坐标轴"
# xy轴范围/位置
ax3d.set_xlim(np.min(points[:, 0]) - 1, np.max(points[:, 0]) + 1)
ax3d.set_ylim(np.min(points[:, 1]) - 1, np.max(points[:, 1]) + 1)
ax3d.set_zlim(np.min(points[:, 2]) - 1, np.max(points[:, 2]) + 1)
# ax3d.set_aspect('auto')  # Set the aspect of the axis scaling, i.e. the ratio of y-unit to x-unit.
ax3d.set_box_aspect([np.ptp(points[:, i])+2 for i in range(3)])

"网格"
ax3d.grid(which='major', axis='both', color='gray', linestyle=':', linewidth=0.5)

plt.show()
