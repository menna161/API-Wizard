import random
import math
import numpy as np
import numbers
import collections
import cv2
import torch


def __call__(self, image, label):
    (h, w) = label.shape
    pad_h = max((self.crop_h - h), 0)
    pad_w = max((self.crop_w - w), 0)
    pad_h_half = int((pad_h / 2))
    pad_w_half = int((pad_w / 2))
    if ((pad_h > 0) or (pad_w > 0)):
        if (self.padding is None):
            raise RuntimeError('segtransform.Crop() need padding while padding argument is None\n')
        image = cv2.copyMakeBorder(image, pad_h_half, (pad_h - pad_h_half), pad_w_half, (pad_w - pad_w_half), cv2.BORDER_CONSTANT, value=self.padding)
        label = cv2.copyMakeBorder(label, pad_h_half, (pad_h - pad_h_half), pad_w_half, (pad_w - pad_w_half), cv2.BORDER_CONSTANT, value=self.ignore_label)
    (h, w) = label.shape
    if (self.crop_type == 'rand'):
        h_off = random.randint(0, (h - self.crop_h))
        w_off = random.randint(0, (w - self.crop_w))
    else:
        h_off = int(((h - self.crop_h) / 2))
        w_off = int(((w - self.crop_w) / 2))
    image = image[(h_off:(h_off + self.crop_h), w_off:(w_off + self.crop_w))]
    label = label[(h_off:(h_off + self.crop_h), w_off:(w_off + self.crop_w))]
    return (image, label)
