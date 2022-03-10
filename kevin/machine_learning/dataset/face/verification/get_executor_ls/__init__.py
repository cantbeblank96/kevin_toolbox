"""
本模块是实现数据集分块生成的核心模块，依赖于执行器 Executor 模块
禁止外部调用
"""
from .by_samples import get_executor_ls_by_samples
from .along_axis import get_executor_ls_along_axis
from .along_diagonal import get_executor_ls_along_diagonal
from .by_block_of_all import get_executor_ls_by_block_of_all
from .by_block_of_triangle import get_executor_ls_by_block_of_triangle
