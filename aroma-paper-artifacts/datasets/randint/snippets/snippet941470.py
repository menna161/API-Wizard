from __future__ import division
import torch
import math
import random
from PIL import Image, ImageOps
import numpy as np
import numbers
import types
import torchvision.transforms.functional as TF


@staticmethod
def get_params(img, scale, ratio):
    'Get parameters for ``crop`` for a random sized crop.\n        Args:\n            img (PIL Image): Image to be cropped.\n            scale (tuple): range of size of the origin size cropped\n            ratio (tuple): range of aspect ratio of the origin aspect ratio cropped\n        Returns:\n            tuple: params (i, j, h, w) to be passed to ``crop`` for a random\n                sized crop.\n        '
    for attempt in range(10):
        area = (img.size[0] * img.size[1])
        target_area = (random.uniform(*scale) * area)
        aspect_ratio = random.uniform(*ratio)
        w = int(round(math.sqrt((target_area * aspect_ratio))))
        h = int(round(math.sqrt((target_area / aspect_ratio))))
        if (random.random() < 0.5):
            (w, h) = (h, w)
        if ((w <= img.size[0]) and (h <= img.size[1])):
            i = random.randint(0, (img.size[1] - h))
            j = random.randint(0, (img.size[0] - w))
            return (i, j, h, w)
    w = min(img.size[0], img.size[1])
    i = ((img.size[1] - w) // 2)
    j = ((img.size[0] - w) // 2)
    return (i, j, w, w)
