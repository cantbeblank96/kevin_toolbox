from .detect_collision_inside_boxes import detect_collision_inside_boxes
from .detect_collision_among_boxes_ls import detect_collision_among_boxes_ls


def detect_collision(**kwargs):
    """
        Adapt the entry of different detection functions
    """
    if "boxes" in kwargs:
        return detect_collision_inside_boxes(**kwargs)
    elif "boxes_ls" in kwargs:
        return detect_collision_among_boxes_ls(**kwargs)
    else:
        raise ValueError(f"parameter boxes or boxes_ls is required!")
