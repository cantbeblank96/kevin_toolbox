import numpy as np

from kevin.math.dimension import coordinates, reshape
from kevin.patches.for_matplotlib import add_trajectory_2d, add_trajectory_3d

import matplotlib.pyplot as plt
import matplotlib.axes._axes as axes
import matplotlib.figure as figure

# 支持中文
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# ------------ 准备数据 ------------ #
# points = coordinates.generate(shape=[4, 4], pattern="z_pattern", output_format="indices_ls")
points = coordinates.generate(shape=[6, 6], pattern="shuffle_inside_block", output_format="indices_ls",
                              kwargs=dict(stride=2, kernel_size=2, seed=1145141919))
# points = coordinates.generate(shape=[3, 3], pattern="normal", output_format="indices_ls",
#                               kwargs=dict(order="F"))

# ------------ 准备画布与图层 ------------ #
fig, ax = plt.subplots(figsize=(8, 8))  # type:figure.Figure, axes.Axes

# ------------ 开启交互模式 ------------ #
plt.ion()
from matplotlib import animation

writer = animation.ImageMagickWriter(
    fps=2,
    metadata=dict(artist='hsu-kevin: kevin-toolbox', comment='contact me with: xukaiming1996@163.com')
)
with writer.saving(fig, "pattern-shuffle_inside_block-stride-2-kernel_size-2-shape-[6,6].gif", dpi=60):
    for end_idx in range(1, len(points) + 1):
        # ------------ 绘制图形元素 ------------ #
        add_trajectory_2d(ax=ax, points=points[:end_idx])

        # ------------ 调整元素属性，处理细节 ------------ #

        "坐标轴"
        # xy轴label
        ax.set_xlabel(xlabel='dim:0', fontdict=dict(fontsize=15, fontfamily='sans-serif', fontstyle='italic'))
        ax.set_ylabel(ylabel='dim:1', fontdict=dict(fontsize=15, fontfamily='sans-serif', fontstyle='italic'))

        # xy轴范围/位置
        margin = 0.5
        ax.set_xlim(np.min(points[:, 0]) - margin, np.max(points[:, 0]) + margin)
        ax.set_ylim(np.min(points[:, 1]) - margin, np.max(points[:, 1]) + margin)
        ax.set_aspect('equal')  # Set the aspect of the axis scaling, i.e. the ratio of y-unit to x-unit.

        # (major)tick
        ax.xaxis.set_ticks(list(set(points[:, 0])), minor=False)  # Set this Axis' tick locations.
        ax.yaxis.set_ticks(list(set(points[:, 1])), minor=False)  # Set this Axis' tick locations.

        "网格"
        ax.grid(which='major', axis='both', color='gray', linestyle=':', linewidth=0.5)

        # jupyter中动态显示需要添加：
        # display.clear_output(wait=True)
        plt.pause(0.5)
        writer.grab_frame()
        "清空画布"
        ax.clear()  # Clear the figure.

# ------------ 关闭交互模式 ------------ #
plt.ioff()
