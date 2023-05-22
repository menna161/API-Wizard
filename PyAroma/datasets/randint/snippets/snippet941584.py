import random
import numpy as np
import torch.utils.data as data
from PIL import Image
import torchvision.transforms as transforms
from abc import ABC, abstractmethod


def get_params(opt, size):
    (w, h) = size
    new_h = h
    new_w = w
    if (opt.preprocess == 'resize_and_crop'):
        new_h = new_w = opt.load_size
    elif (opt.preprocess == 'scale_width_and_crop'):
        new_w = opt.load_size
        new_h = ((opt.load_size * h) // w)
    x = random.randint(0, np.maximum(0, (new_w - opt.crop_size)))
    y = random.randint(0, np.maximum(0, (new_h - opt.crop_size)))
    flip = (random.random() > 0.5)
    return {'crop_pos': (x, y), 'flip': flip}
