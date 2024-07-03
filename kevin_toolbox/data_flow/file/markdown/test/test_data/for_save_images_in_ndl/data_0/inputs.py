import os
import cv2
import torch
from PIL import Image

image_path = os.path.join(os.path.dirname(__file__), "80.jpg")

table_s = {
    "read by": ["image"],
    "cv2": [
        cv2.imread(image_path)
    ],
    "torch": [
        torch.from_numpy(cv2.imread(image_path))
    ],
    "pil": [
        Image.open(image_path)
    ],
    "else": [None]
}

setting_s = {
    "": {"b_is_rgb": False, "saved_image_format": ".jpg"},
    ":pil": {"b_is_rgb": True, "saved_image_format": ".png"}
}