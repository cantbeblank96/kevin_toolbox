import pytest
from kevin.patches.for_test import check_consistency

import torch
import numpy as np

from kevin.math.dimension import concat_and_split
from kevin.math.utils import get_function_table_for_array_and_tensor, get_crop_by_box


@pytest.mark.parametrize("x_shape, boxes, beg_axis",
                         list(zip([[3, 16, 16, 10], [4, 4]],
                                  [
                                      np.array([
                                          [[0, 0],
                                           [4, 4]],
                                          [[0, 4],
                                           [4, 16]],
                                          [[4, 0],
                                           [16, 4]],
                                          [[4, 4],
                                           [16, 16]],
                                      ]),
                                      np.array([
                                          [[0, 0],
                                           [4, 2]],
                                          [[4, 1],
                                           [4, 1]],
                                          [[0, 2],
                                           [4, 4]],
                                          [[4, 2],
                                           [4, 4]],
                                      ]),
                                  ],
                                  [1, 0]))[:])
def test_computational_tree(x_shape, boxes, beg_axis):
    print("test: use concat_and_split.node to build computational_tree")

    boxes = np.sort(boxes, axis=1)
    end_axis = beg_axis + boxes.shape[-1] - 1

    for size in range(1, len(boxes) + 1):
        # 测试各种 box 的组合
        print(f'size : {size}')
        box_ls = list(boxes[np.random.choice(np.arange(len(boxes)), size=size, replace=False)])

        # 同时测试对 np.array 和 torch.tensor 的兼容性
        x_ls = [np.arange(np.prod(x_shape)).reshape(x_shape),
                torch.arange(np.prod(x_shape)).reshape(x_shape)]
        for x in x_ls:
            _, function_table = get_function_table_for_array_and_tensor(x)
            concat, flatten = function_table["concat"], function_table["flatten"]

            tree = concat_and_split.Node(box_ls=box_ls)

            print("build_tree")
            tree.build_tree()
            tree.init_tree()
            tree.print_tree()
            assert len(tree.get_leaf_nodes()) == len(box_ls)

            expected_whole = flatten(x, axis_0=beg_axis, axis_1=end_axis)
            indices = np.arange(np.prod(x_shape[beg_axis:end_axis + 1])).reshape(x_shape[beg_axis:end_axis + 1])
            indices = np.sort(
                np.concatenate([i.flatten() for i in get_crop_by_box(x=indices, box_ls=box_ls, beg_axis=0)]))
            expected_whole = expected_whole[tuple([slice(None, None)] * beg_axis + [indices])]
            print(expected_whole.shape)

            print("split")
            tree.var = expected_whole
            tree.split(beg_axis=beg_axis)
            #
            for node in tree.get_leaf_nodes():
                expected_crop = get_crop_by_box(x=x, box_ls=node.details["box_ls"], beg_axis=beg_axis)[0]
                check_consistency(node.var, expected_crop)

            print("clear_tree")
            tree.clear_tree(depths=[0, 1])
            assert tree.var is None

            print("concat")
            tree.concat(beg_axis=beg_axis)
            #
            check_consistency(tree.var, expected_whole)


@pytest.mark.parametrize("x_shape, boxes, beg_axis",
                         list(zip([[3, 16, 16, 10], [4, 4]],
                                  [
                                      np.array([
                                          [[0, 0],
                                           [4, 4]],
                                          [[0, 4],
                                           [4, 16]],
                                          [[4, 0],
                                           [16, 4]],
                                          [[4, 4],
                                           [16, 16]],
                                      ]),
                                      np.array([
                                          [[0, 0],
                                           [4, 2]],
                                          [[4, 1],
                                           [4, 1]],
                                          [[0, 2],
                                           [4, 4]],
                                          [[4, 2],
                                           [4, 4]],
                                      ]),
                                  ],
                                  [1, 0]))[:])
def test_split_and_concat_crops(x_shape, boxes, beg_axis):
    print("test: concat_crops_into_whole and split_whole_into_crops")

    boxes = np.sort(boxes, axis=1)
    end_axis = beg_axis + boxes.shape[-1] - 1

    for size in range(1, len(boxes) + 1):
        # 测试各种 box 的组合
        print(f'size : {size}')
        box_ls = list(boxes[np.random.choice(np.arange(len(boxes)), size=size, replace=False)])

        # 同时测试对 np.array 和 torch.tensor 的兼容性
        x_ls = [np.arange(np.prod(x_shape)).reshape(x_shape),
                torch.arange(np.prod(x_shape)).reshape(x_shape)]
        for x in x_ls:
            _, function_table = get_function_table_for_array_and_tensor(x)
            concat, flatten = function_table["concat"], function_table["flatten"]

            expected_whole = flatten(x, axis_0=beg_axis, axis_1=end_axis)
            indices = np.arange(np.prod(x_shape[beg_axis:end_axis + 1])).reshape(x_shape[beg_axis:end_axis + 1])
            indices = np.sort(
                np.concatenate([i.flatten() for i in get_crop_by_box(x=indices, box_ls=box_ls, beg_axis=0)]))
            expected_whole = expected_whole[tuple([slice(None, None)] * beg_axis + [indices])]
            print(expected_whole.shape)

            print("split")
            details = concat_and_split.split_whole_into_crops(whole=expected_whole, box_ls=box_ls, beg_axis=beg_axis,
                                                              return_details=True)
            for box, crop in zip(sorted(box_ls, key=lambda u: u[0].tolist()), details["crop_ls"]):
                expected_crop = get_crop_by_box(x=x, box_ls=[box], beg_axis=beg_axis)[0]
                check_consistency(crop, expected_crop)

            print("concat")
            details.pop("whole")
            details = concat_and_split.concat_crops_into_whole(**details, return_details=True)
            #
            check_consistency(details["whole"], expected_whole)
