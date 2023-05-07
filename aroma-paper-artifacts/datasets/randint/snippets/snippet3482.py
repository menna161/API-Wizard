from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import numpy as np
from random import randint


def random_crop(img, boxes, box_scale, round_boxes=True, max_crop_fraction=0.1):
    "\n    Randomly crops the image\n    :param img: PIL image\n    :param boxes: Ground truth boxes\n    :param box_scale: This is the scale that the boxes are at (e.g. 1024 wide). We'll preserve that ratio\n    :param round_boxes: Set this to true if we're going to round the boxes to ints\n    :return: Cropped image, new boxes\n    "
    (w, h) = img.size
    max_crop_w = int((w * max_crop_fraction))
    max_crop_h = int((h * max_crop_fraction))
    boxes_scaled = ((boxes * max(w, h)) / box_scale)
    max_to_crop_top = min(int(boxes_scaled[(:, 1)].min()), max_crop_h)
    max_to_crop_left = min(int(boxes_scaled[(:, 0)].min()), max_crop_w)
    max_to_crop_right = min(int((w - boxes_scaled[(:, 2)].max())), max_crop_w)
    max_to_crop_bottom = min(int((h - boxes_scaled[(:, 3)].max())), max_crop_h)
    crop_top = randint(0, max(max_to_crop_top, 0))
    crop_left = randint(0, max(max_to_crop_left, 0))
    crop_right = randint(0, max(max_to_crop_right, 0))
    crop_bottom = randint(0, max(max_to_crop_bottom, 0))
    img_cropped = img.crop((crop_left, crop_top, (w - crop_right), (h - crop_bottom)))
    new_boxes = ((box_scale / max(img_cropped.size)) * np.column_stack(((boxes_scaled[(:, 0)] - crop_left), (boxes_scaled[(:, 1)] - crop_top), (boxes_scaled[(:, 2)] - crop_left), (boxes_scaled[(:, 3)] - crop_top))))
    if round_boxes:
        new_boxes = np.round(new_boxes).astype(np.int32)
    return (img_cropped, new_boxes)
