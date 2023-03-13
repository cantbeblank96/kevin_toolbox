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
# points = coordinates.generate(shape=[3, 3, 2], pattern="normal", output_format="indices_ls",
#                               kwargs=dict(order="C"))

# ------------ 准备画布与图层 ------------ #
fig = plt.figure(figsize=(8, 8))  # type:figure.Figure
ax3d = fig.add_subplot(1, 1, 1, projection='3d')  # type:Axes3D

# ------------ 开启交互模式 ------------ #
plt.ion()
from matplotlib import animation

writer = animation.ImageMagickWriter(
    fps=2,
    metadata=dict(artist='hsu-kevin: kevin-toolbox', comment='contact me with: xukaiming1996@163.com')
)
with writer.saving(fig, "pattern-shuffle_inside_block-stride-2-kernel_size-2-shape-[4,4,4].gif", dpi=60):
    for end_idx in range(1, len(points) + 1):
        # ------------ 绘制图形元素 ------------ #
        add_trajectory_3d(ax3d=ax3d, points=points[:end_idx])

        # ------------ 调整元素属性，处理细节 ------------ #

        "坐标轴"
        # xy轴label
        ax3d.set_xlabel(xlabel='dim:0', fontdict=dict(fontsize=15, fontfamily='sans-serif', fontstyle='italic'))
        ax3d.set_ylabel(ylabel='dim:1', fontdict=dict(fontsize=15, fontfamily='sans-serif', fontstyle='italic'))
        ax3d.set_zlabel(zlabel='dim:2', fontdict=dict(fontsize=15, fontfamily='sans-serif', fontstyle='italic'))

        # xy轴范围/位置
        margin = 0.5
        ax3d.set_xlim(np.min(points[:, 0]) - margin, np.max(points[:, 0]) + margin)
        ax3d.set_ylim(np.min(points[:, 1]) - margin, np.max(points[:, 1]) + margin)
        ax3d.set_zlim(np.min(points[:, 2]) - margin, np.max(points[:, 2]) + margin)
        # ax3d.set_aspect('auto')  # Set the aspect of the axis scaling, i.e. the ratio of y-unit to x-unit.
        ax3d.set_box_aspect([np.ptp(points[:, i]) + 2 * margin for i in range(3)])

        # (major)tick
        ax3d.xaxis.set_ticks(list(set(points[:, 0])), minor=False)  # Set this Axis' tick locations.
        ax3d.yaxis.set_ticks(list(set(points[:, 1])), minor=False)  # Set this Axis' tick locations.
        ax3d.zaxis.set_ticks(list(set(points[:, 2])), minor=False)  # Set this Axis' tick locations.

        "网格"
        ax3d.grid(which='major', axis='both', color='gray', linestyle=':', linewidth=0.5)

        "改变视角"
        # 采用view_init可以改变3D图像的视角，该命令有两个参数，elevation纬度和azimuth经度（度数）
        # ax3d.view_init(elev=-20, azim=10)

        # jupyter中动态显示需要添加：
        # display.clear_output(wait=True)
        plt.pause(0.5)
        writer.grab_frame()
        "清空画布"
        ax3d.clear()  # Clear the figure.

# ------------ 关闭交互模式 ------------ #
plt.ioff()
