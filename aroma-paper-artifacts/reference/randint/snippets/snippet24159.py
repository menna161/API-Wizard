import cv2
import numpy as np


def get_crop_bbox(crop_size, img):
    'Random cropping - bounding box.'
    margin_h = max((img.shape[0] - crop_size[0]), 0)
    margin_w = max((img.shape[1] - crop_size[1]), 0)
    offset_h = rng.randint(0, (margin_h + 1))
    offset_w = rng.randint(0, (margin_w + 1))
    (crop_y1, crop_y2) = (offset_h, (offset_h + crop_size[0]))
    (crop_x1, crop_x2) = (offset_w, (offset_w + crop_size[1]))
    return (crop_y1, crop_y2, crop_x1, crop_x2)
