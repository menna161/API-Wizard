import torch
import random
import cv2
import collections
import numpy as np
from skimage.filters import gaussian
from scipy.ndimage import zoom as scizoom
import torchvision.transforms as transforms


def augment_random_translate(img, random_factor=0.1):
    random_translation_range = int((img.size(1) * random_factor))
    pad_size = (random_translation_range // 2)
    padded_tensor = torch.nn.functional.pad(img, (pad_size, pad_size, pad_size, pad_size))
    (h, w) = (img.size(1), img.size(2))
    (padded_h, padded_w) = (padded_tensor.size(1), padded_tensor.size(2))
    offset_h = random.randint(0, (padded_h - h))
    offset_w = random.randint(0, (padded_w - w))
    img = padded_tensor[(:, offset_h:(h + offset_h), offset_w:(w + offset_w))]
    return img
