import os
import cv2
import numpy as np
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.patches.for_matplotlib import common_charts

temp_dir = os.path.join(os.path.dirname(__file__), "temp")


def test_plot_bars():
    output_path = common_charts.plot_bars(data_s={
        'a': [1.5, 2, 3, 4, 5],
        'b': [5, 4, 3, 2, 1],
        'c': [1, 2, 3, 4, 5]},
        title='test_plot_bars', x_name='a', output_dir=temp_dir,
        b_generate_record=True,
        suffix=".png"
    )
    output_path_1 = common_charts.plot_from_record(
        input_path=output_path + ".record.tar",
        output_dir=os.path.join(temp_dir, "recover")
    )
    check_consistency(cv2.imread(output_path), cv2.imread(output_path_1))


def test_plot_confusion_matrix():
    # 示例真实标签和预测标签
    y_true = np.array([0, 1, 2, 0, 1, 2, 0, 1, 2, 5])
    y_pred = np.array([0, 2, 1, 0, 2, 1, 0, 1, 1, 5])

    output_path = common_charts.plot_confusion_matrix(
        data_s={'a': y_true, 'b': y_pred},
        title='test_plot_confusion_matrix', gt_name='a', pd_name='b',
        label_to_value_s={"A": 5, "B": 0, "C": 1, "D": 2, "E": 3},
        output_dir=os.path.join(os.path.dirname(__file__), "temp"),
        replace_zero_division_with=-1,
        normalize="all",
        b_generate_record=True
    )
    output_path_1 = common_charts.plot_from_record(
        input_path=output_path + ".record.tar",
        output_dir=os.path.join(temp_dir, "recover")
    )
    check_consistency(cv2.imread(output_path), cv2.imread(output_path_1))


def test_plot_distribution():
    output_path = common_charts.plot_distribution(
        data_s={
            'a': [1, 2, 3, 4, 5, 3, 2, 1],
            'c': [1, 2, 3, 4, 5, 0, 0, 0]},
        title='test_plot_distribution', x_name_ls=['a', 'c'], type_="category",
        output_dir=os.path.join(os.path.dirname(__file__), "temp"),
        b_generate_record=True
    )
    output_path_1 = common_charts.plot_from_record(
        input_path=output_path + ".record.tar",
        output_dir=os.path.join(temp_dir, "recover")
    )
    check_consistency(cv2.imread(output_path), cv2.imread(output_path_1))


def test_plot_lines():
    output_path = common_charts.plot_lines(
        data_s={
            'a': [1, 2, 3, 4, 5],
            'b': [5, 4, 3, 2, 1],
            'c': [1, 2, 3, 4, 5]},
        title='test_plot_lines',
        x_name='a', output_dir=os.path.join(os.path.dirname(__file__), "temp"),
        b_generate_record=True
    )

    output_path_1 = common_charts.plot_from_record(
        input_path=output_path + ".record.tar",
        output_dir=os.path.join(temp_dir, "recover")
    )
    check_consistency(cv2.imread(output_path), cv2.imread(output_path_1))


def test_plot_scatters():
    data_s_ = dict(
        x=[1, 2, 3, 4, 5],
        y=[2, 4, 6, 8, 10],
        categories=['A', 'B', 'A', 'B', 'A']
    )

    output_path = common_charts.plot_scatters(
        data_s=data_s_, title='test_plot_scatters', x_name='x', y_name='y', cate_name='categories',
        output_dir=os.path.join(os.path.dirname(__file__), "temp"),
        b_generate_record=True
    )

    output_path_1 = common_charts.plot_from_record(
        input_path=output_path + ".record.tar",
        output_dir=os.path.join(temp_dir, "recover")
    )
    check_consistency(cv2.imread(output_path), cv2.imread(output_path_1))


def test_plot_scatters_matrix():
    data_s_ = dict(
        x=[1, 2, 3, 4, 5],
        y=[2, 4, 6, 8, 10],
        z=[2, 4, 6, 8, 10],
        categories=['A', 'B', 'A', 'B', 'A'],
        title='test',
    )

    output_path = common_charts.plot_scatters_matrix(
        data_s=data_s_, title='test_plot_scatters_matrix', x_name_ls=['y', 'x', 'z'], cate_name='categories',
        cate_color_s={'A': 'red', 'B': 'blue'},
        output_dir=os.path.join(os.path.dirname(__file__), "temp"),
        b_generate_record=True
    )

    output_path_1 = common_charts.plot_from_record(
        input_path=output_path + ".record.tar",
        output_dir=os.path.join(temp_dir, "recover")
    )
    check_consistency(cv2.imread(output_path), cv2.imread(output_path_1))
