import os
import numpy as np
import torch
import torch.nn as nn
import cv2
import random
import PIL
from PIL import Image
from torch.utils.data import Sampler
import torchvision.transforms as transforms
import math
import torchvision.datasets as datasets


def __call__(self, img):
    assert isinstance(img, PIL.Image.Image)
    img = np.asarray(img, dtype=np.uint8)
    (H, W, C) = img.shape
    well_cropped = False
    for _ in range(self.max_attempts):
        crop_area = ((H * W) * random.uniform(self.scale[0], self.scale[1]))
        crop_edge = round(math.sqrt(crop_area))
        dH = (H - crop_edge)
        dW = (W - crop_edge)
        crop_left = random.randint(min(dW, 0), max(dW, 0))
        crop_top = random.randint(min(dH, 0), max(dH, 0))
        if ((dH >= 0) and (dW >= 0)):
            well_cropped = True
            break
    crop_bottom = (crop_top + crop_edge)
    crop_right = (crop_left + crop_edge)
    if well_cropped:
        crop_image = img[crop_top:crop_bottom, :, :][:, crop_left:crop_right, :]
    else:
        roi_top = max(crop_top, 0)
        padding_top = (roi_top - crop_top)
        roi_bottom = min(crop_bottom, H)
        padding_bottom = (crop_bottom - roi_bottom)
        roi_left = max(crop_left, 0)
        padding_left = (roi_left - crop_left)
        roi_right = min(crop_right, W)
        padding_right = (crop_right - roi_right)
        roi_image = img[roi_top:roi_bottom, :, :][:, roi_left:roi_right, :]
        crop_image = cv2.copyMakeBorder(roi_image, padding_top, padding_bottom, padding_left, padding_right, borderType=cv2.BORDER_CONSTANT, value=0)
    random.choice([1])
    target_image = cv2.resize(crop_image, (self.target_size, self.target_size), interpolation=cv2.INTER_LINEAR)
    target_image = PIL.Image.fromarray(target_image.astype('uint8'))
    return target_image
