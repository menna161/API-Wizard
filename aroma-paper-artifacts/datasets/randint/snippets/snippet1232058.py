from __future__ import division
import torch
import math
import sys
import random
from PIL import Image
import numpy as np
import numbers
import types
import collections
import warnings
import torchvision.transforms.functional as F
import accimage


@staticmethod
def get_params(img, output_size):
    'Get parameters for ``crop`` for a random crop.\n\n        Args:\n            img (PIL Image): Image to be cropped.\n            output_size (tuple): Expected output size of the crop.\n\n        Returns:\n            tuple: params (i, j, h, w) to be passed to ``crop`` for random crop.\n        '
    (w, h) = _get_image_size(img)
    (th, tw) = output_size
    if ((w == tw) and (h == th)):
        return (0, 0, h, w)
    i = random.randint(0, (h - th))
    j = random.randint(0, (w - tw))
    return (i, j, th, tw)
