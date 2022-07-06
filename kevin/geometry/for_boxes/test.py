import pytest
import numpy as np
# 待测试模块
from kevin.geometry import for_boxes
# 测试数据
from kevin.geometry.for_boxes.test_data.data_all import boxes_ls, relations_ls


@pytest.mark.parametrize("boxes, expected",
                         zip(boxes_ls, relations_ls))
def test_cal_iou(boxes, expected):
    print("test for_boxes.cal_iou()")

    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            iou = for_boxes.cal_iou(box_0=boxes[i], box_1=boxes[j])
            print(f"between box_{i} and box_{j} iou is {iou}")
            if j in expected["overlapped"].get(i, set()) or i in expected["overlapped"].get(j, set()):
                assert iou > 0
            else:
                assert iou == 0


@pytest.mark.parametrize("boxes",
                         boxes_ls)
def test_convert(boxes):
    print("test for_boxes.convert_from_coord_to_grid_index()")

    print("grid_coverage_mode closed with ticks")
    ticks = for_boxes.get_ticks(boxes=boxes)
    settings_for_grid = dict(mode="closed", ticks=ticks)
    grids = for_boxes.convert_from_coord_to_grid_index(boxes=boxes, settings_for_grid=settings_for_grid)

    boxes_recover = for_boxes.convert_from_coord_to_grid_index(boxes=grids, settings_for_grid=settings_for_grid,
                                                               reverse=True)

    boxes_input = np.sort(boxes, axis=1)
    assert np.max(np.abs(boxes_recover - boxes_input)) == 0

    print("grid_coverage_mode closed with grid_size")
    temp_ls = [boxes]
    settings_for_grid = dict(
        mode="closed",
        grid_size=[[10, 10, 20, 50, 70, 100]] * boxes.shape[-1],
        offset=-4
    )
    for _ in range(2):
        grids = for_boxes.convert_from_coord_to_grid_index(boxes=temp_ls[-1], settings_for_grid=settings_for_grid)
        boxes_recover = for_boxes.convert_from_coord_to_grid_index(boxes=grids, settings_for_grid=settings_for_grid,
                                                                   reverse=True)
        temp_ls.append(boxes_recover)
    assert np.max(np.abs(temp_ls[-1] - temp_ls[-2])) == 0

    print("grid_coverage_mode open")
    temp_ls = [boxes]
    settings_for_grid = dict(mode="open", grid_size=4, offset=-4)
    for _ in range(2):
        grids = for_boxes.convert_from_coord_to_grid_index(boxes=temp_ls[-1], settings_for_grid=settings_for_grid)
        boxes_recover = for_boxes.convert_from_coord_to_grid_index(boxes=grids, settings_for_grid=settings_for_grid,
                                                                   reverse=True)
        temp_ls.append(boxes_recover)
    assert np.max(np.abs(temp_ls[-1] - temp_ls[-2])) == 0


test_input = []
for b, r in zip(boxes_ls, relations_ls):
    for c in [0, 10000]:
        for d in [True, False]:
            test_input.append((b, c, d, r))


@pytest.mark.parametrize("boxes, correction_factor, duplicate_records, expected",
                         test_input)
def test_detect_collision(boxes, correction_factor, duplicate_records, expected):
    print("test for_boxes.detect_collision()")

    res = for_boxes.detect_collision(boxes=boxes, complexity_correction_factor_for_aixes_check=correction_factor,
                                     duplicate_records=duplicate_records)
    print(f"collision_groups {res}")

    cal_collision_num = lambda collision_groups: sum([len(v_ls) for k, v_ls in collision_groups.items()])

    # 检查碰撞数量
    if duplicate_records:
        assert cal_collision_num(res) / 2 == cal_collision_num(expected["collided"])
    else:
        assert cal_collision_num(res) == cal_collision_num(expected["collided"])
    # 具体检查
    for i, j_ls in expected["collided"].items():
        for j in j_ls:
            if duplicate_records:
                assert j in res.get(i, set()) and i in res.get(j, set())
            else:
                assert j in res.get(i, set()) or i in res.get(j, set())


@pytest.mark.parametrize("boxes, relations",
                         zip(boxes_ls, relations_ls))
def test_boolean_algebra(boxes, relations):
    print("test for_boxes.boolean_algebra()")

    for i in range(len(boxes)):
        for j in range(len(boxes)):
            boxes_ls = [boxes[[i]], boxes[[j]]]
            details = for_boxes.cal_iou(box_0=boxes_ls[0][0], box_1=boxes_ls[1][0], return_details=True)
            # test binary_operation
            bi_operation_choices = ['or', 'and', 'diff']
            for b_ in bi_operation_choices:
                res_boxes = for_boxes.boolean_algebra(boxes_ls=boxes_ls, binary_operation_ls=[b_],
                                                      unary_operation_ls=[None, None])
                # 统计面积
                area = for_boxes.cal_area(res_boxes)
                #
                if b_ == "or":
                    assert area == details["union"]["area"]
                elif b_ == "and":
                    assert area == details["intersection"]["area"]
                elif b_ == "diff":
                    assert area == details["box_0"]["area"] - details["intersection"]["area"]
            # test unary_operation
            res_boxes_0 = for_boxes.boolean_algebra(boxes_ls=boxes_ls, binary_operation_ls=['diff'],
                                                    unary_operation_ls=[None, None])
            res_boxes_1 = for_boxes.boolean_algebra(boxes_ls=boxes_ls, binary_operation_ls=['and'],
                                                    unary_operation_ls=[None, 'not'])
            # 统计面积
            area_0 = for_boxes.cal_area(res_boxes_0)
            area_1 = for_boxes.cal_area(res_boxes_1)
            assert area_0 == area_1


@pytest.mark.parametrize("boxes, relations",
                         zip(boxes_ls, relations_ls))
def test_detect_overlap(boxes, relations):
    print("test for_boxes.detect_overlap()")

    node_ls = for_boxes.detect_overlap(boxes_ls=[box[None, ...] for box in boxes])
    area = 0
    for node in node_ls:
        area += for_boxes.cal_area(boxes=node.description["by_boxes"]) * len(
            node.description["by_item_ids"]["intersection"])
    assert for_boxes.cal_area(boxes=boxes) == area
