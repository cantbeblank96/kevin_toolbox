import os
import openpyxl
import numpy as np
from kevin_toolbox.data_flow.file import excel

temp_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "test_data/temp")
os.makedirs(temp_dir, exist_ok=True)


def test_write_with_matrix():
    mat = np.random.rand(4, 3)
    excel.write_with_matrix(file_path=os.path.join(temp_dir, 'test.xlsx'), sheet_name="566666", matrix=mat,
                            column_label_ls=['红', '绿', '蓝'],
                            row_label_ls=['1 1', '1 2', '2 1', '2 2'],
                            column_title="这里是column_title 啊啊啊",
                            row_title="这里是row_title 啊啊啊", main_title="总标题 total")

    mat_2 = np.ones([4, 4])
    wb = excel.write_with_matrix(file_obj=openpyxl.Workbook(), sheet_name="result结构说明",
                                 matrix=mat_2, column_label_ls=['列', '向', '标', '签'],
                                 row_label_ls=['行', '向', '标', '签'], column_title="转移目标（预测）",
                                 row_title="转移起点（已知）", main_title="总标题")
    wb.save(os.path.join(temp_dir, 'test2.xlsx'))
