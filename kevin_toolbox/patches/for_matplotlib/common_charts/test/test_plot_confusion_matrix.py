import os
import numpy as np
from kevin_toolbox.data_flow.file import markdown
from kevin_toolbox.patches.for_matplotlib.common_charts import plot_confusion_matrix

output_dir = os.path.join(os.path.dirname(__file__), "temp")


def test_plot_confusion_matrix_0():
    # 示例真实标签和预测标签
    y_true = np.array([0, 1, 2, 0, 1, 2, 0, 1, 2, 5])  # 预测的类别
    y_pred = np.array([0, 2, 1, 0, 2, 1, 0, 1, 1, 5])

    doc = "# 演示\n\n"

    doc += "## recall\n\n"
    out_file, cfm = plot_confusion_matrix(
        data_s={'gt': y_true, 'pd': y_pred},
        title='recall', gt_name='gt', pd_name='pd',
        label_to_value_s={"A": 0, "B": 1, "C": 2, "D": 5},
        # label_idx 到 label_name 的映射，不指定时候直接用 label_idx 作为 label_name
        output_dir=os.path.join(output_dir, "plots"),
        b_return_cfm=True,
        normalize="true"  # 按照 gt进行归一化，此时对角线上的值就是 recall
    )
    doc += markdown.generate_link(name=os.path.basename(out_file), target=os.path.relpath(out_file, start=output_dir),
                                  type_="image") + "\n\n"
    doc += f'```\n{cfm}\n```\n\n'

    doc += "## precision\n\n"
    out_file, cfm = plot_confusion_matrix(
        data_s={'gt': y_true, 'pd': y_pred},
        title='precision', gt_name='gt', pd_name='pd',
        output_dir=os.path.join(output_dir, "plots"),
        b_return_cfm=True,
        normalize="pred"  # 按照 pd 进行归一化，此时对角线上的值就是 precision
    )
    doc += markdown.generate_link(name=os.path.basename(out_file), target=os.path.relpath(out_file, start=output_dir),
                                  type_="image") + "\n\n"
    doc += f'```\n{cfm}\n```\n\n'

    with open(os.path.join(output_dir, "demo.md"), "w", encoding="utf-8") as f:
        f.write(doc)


def test_plot_confusion_matrix_1():
    """
        测试不同内容的 label_to_value_s 参数
    """
    y_true = np.array([0, 1, 2, 0, 1, 2, 0, 1, 2, 5])
    y_pred = np.array([0, 2, 1, 0, 2, 1, 0, 1, 1, 5])

    doc = "# 演示\n\n"

    for i,label_to_value_s in enumerate([
        {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5},  # label_to_value_s 中含有部分 data_s 中未见的 label_idx
        {"A": 0, "C": 2},  # label_to_value_s 中缺少 data_s 中已有的 label_idx
        {"C": 2, "D": 3, "E": 4, "F": 5}  # label_to_value_s 中缺少 data_s 中已有的 label_idx，同时中含有部分 data_s 中未见的 label_idx
    ]):
        out_file, cfm = plot_confusion_matrix(
            data_s={'gt': y_true, 'pd': y_pred},
            title=f'image_{i}', gt_name='gt', pd_name='pd',
            label_to_value_s=label_to_value_s,
            output_dir=os.path.join(output_dir, "plots_1"),
            b_return_cfm=True,
            normalize="true"
        )
        doc += markdown.generate_link(name=os.path.basename(out_file),
                                      target=os.path.relpath(out_file, start=output_dir),
                                      type_="image") + "\n\n"
        doc += f'label_to_value_s:\n\n```\n{label_to_value_s}\n```\n\n'

    with open(os.path.join(output_dir, "demo_1.md"), "w", encoding="utf-8") as f:
        f.write(doc)
