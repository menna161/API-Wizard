import mmcv
import numpy as np
from numpy import random
from mmdet.core.evaluation.bbox_overlaps import bbox_overlaps


def __call__(self, img, boxes, labels):
    if random.randint(2):
        delta = random.uniform((- self.brightness_delta), self.brightness_delta)
        img += delta
    mode = random.randint(2)
    if (mode == 1):
        if random.randint(2):
            alpha = random.uniform(self.contrast_lower, self.contrast_upper)
            img *= alpha
    img = mmcv.bgr2hsv(img)
    if random.randint(2):
        img[(..., 1)] *= random.uniform(self.saturation_lower, self.saturation_upper)
    if random.randint(2):
        img[(..., 0)] += random.uniform((- self.hue_delta), self.hue_delta)
        img[(..., 0)][(img[(..., 0)] > 360)] -= 360
        img[(..., 0)][(img[(..., 0)] < 0)] += 360
    img = mmcv.hsv2bgr(img)
    if (mode == 0):
        if random.randint(2):
            alpha = random.uniform(self.contrast_lower, self.contrast_upper)
            img *= alpha
    if random.randint(2):
        img = img[(..., random.permutation(3))]
    return (img, boxes, labels)
