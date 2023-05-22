import mxnet as mx
import numpy as np
import cv2
import os
from ...utils.dataset_tools import VOC as vocUtils
import multiprocessing as mp


def load_img_sp(image_src, superpixel_src, target_size, scale, mirror, rand_crop):
    img = cv2.imread(image_src)
    (h, w) = img.shape[:2]
    if (superpixel_src is None):
        sp = np.zeros((h, w, 3), np.uint8)
    else:
        sp = cv2.imread(superpixel_src)
    if (scale != 1):
        h = int(((h * scale) + 0.5))
        w = int(((w * scale) + 0.5))
        img = cv2.resize(img, (w, h))
        sp = cv2.resize(sp, (w, h), interpolation=cv2.INTER_NEAREST)
    sp = sp.astype(np.int32)
    sp = ((sp[(..., 0)] + (sp[(..., 1)] * 256)) + (sp[(..., 2)] * 65536))
    if mirror:
        img = img[(:, ::(- 1))]
        sp = sp[(:, ::(- 1))]
    pad_h = max((target_size - h), 0)
    pad_w = max((target_size - w), 0)
    if ((pad_h > 0) or (pad_w > 0)):
        img = cv2.copyMakeBorder(img, 0, pad_h, 0, pad_w, cv2.BORDER_CONSTANT, value=(127, 127, 127))
        sp = cv2.copyMakeBorder(sp, 0, pad_h, 0, pad_w, cv2.BORDER_CONSTANT, value=(int(sp.max()) + 1))
        (h, w) = img.shape[:2]
    if rand_crop:
        h_bgn = np.random.randint(0, ((h - target_size) + 1))
        w_bgn = np.random.randint(0, ((w - target_size) + 1))
    else:
        h_bgn = ((h - target_size) // 2)
        w_bgn = ((w - target_size) // 2)
    img = img[(h_bgn:(h_bgn + target_size), w_bgn:(w_bgn + target_size))]
    sp = sp[(h_bgn:(h_bgn + target_size), w_bgn:(w_bgn + target_size))]
    sp_vals = np.unique(sp)
    sp_lookup = np.zeros(((sp_vals.max() + 1),), np.int32)
    sp_lookup[sp_vals] = np.random.permutation(len(sp_vals))
    sp = sp_lookup[sp.ravel()].reshape(sp.shape)
    return (img, sp)
