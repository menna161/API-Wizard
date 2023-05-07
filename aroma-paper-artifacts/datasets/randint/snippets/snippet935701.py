import mmcv
import numpy as np
from numpy import random
from mmdet.core.evaluation.bbox_overlaps import bbox_overlaps


def __call__(self, img, boxes, labels):
    if random.randint(2):
        return (img, boxes, labels)
    (h, w, c) = img.shape
    ratio = random.uniform(self.min_ratio, self.max_ratio)
    expand_img = np.full((int((h * ratio)), int((w * ratio)), c), self.mean).astype(img.dtype)
    left = int(random.uniform(0, ((w * ratio) - w)))
    top = int(random.uniform(0, ((h * ratio) - h)))
    expand_img[(top:(top + h), left:(left + w))] = img
    img = expand_img
    boxes += np.tile((left, top), 2)
    return (img, boxes, labels)
