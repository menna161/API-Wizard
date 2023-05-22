import mxnet as mx
import numpy as np
import cv2
import os
from ...utils.dataset_tools import VOC as vocUtils
import multiprocessing as mp


def load_img(image_src, target_size, scale, mirror, rand_crop):
    img = cv2.imread(image_src)
    (h, w) = img.shape[:2]
    if (scale != 1):
        h = int(((h * scale) + 0.5))
        w = int(((w * scale) + 0.5))
        img = cv2.resize(img, (w, h))
    if mirror:
        img = img[(:, ::(- 1))]
    pad_h = max((target_size - h), 0)
    pad_w = max((target_size - w), 0)
    if ((pad_h > 0) or (pad_w > 0)):
        img = cv2.copyMakeBorder(img, 0, pad_h, 0, pad_w, cv2.BORDER_CONSTANT, value=(127, 127, 127))
        (h, w) = img.shape[:2]
    if rand_crop:
        h_bgn = np.random.randint(0, ((h - target_size) + 1))
        w_bgn = np.random.randint(0, ((w - target_size) + 1))
    else:
        h_bgn = ((h - target_size) // 2)
        w_bgn = ((w - target_size) // 2)
    img = img[(h_bgn:(h_bgn + target_size), w_bgn:(w_bgn + target_size))]
    return img
