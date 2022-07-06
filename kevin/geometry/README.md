### 数据结构

立方体：

- box
  - <2 axis np.array> 矩形/长方体/超立方体
  - shape [2, dimensions]
    - 各个维度的意义为：
      - 2：          box的两个轴对称点
      - dimensions： 坐标有多少个维度
- boxes
  - <3 axis np.array> 一系列的 box
  - shape [batch_size, 2, dimensions]
    - 各个维度的意义为：
      - batch_size： 有多少个 box
      - 2：          box的两个轴对称点
      - dimensions： 坐标有多少个维度
- box_ls
  - <list of box>



坐标

- ticks
  - <list of np.array> 各个维度/坐标轴上的坐标刻度



几何关系

- collision_groups
  - <dict of integers set> 碰撞对
  - 其中的第 i 个 set 记录了第 i 个 item 与其他哪些 items 存在碰撞
    - 比如：  collision_groups[0] = {1, 2} 表示0号 item 与1、2号 item 发生了碰撞
