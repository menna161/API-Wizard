import logging
import numpy as np
import os
import math
import random
import torch
import torchvision
from PIL import Image
from torch.utils.data import SubsetRandomSampler, Sampler, Subset, ConcatDataset
import torch.distributed as dist
from torchvision.transforms import transforms
from sklearn.model_selection import StratifiedShuffleSplit
from theconf import Config as C
from FastAutoAugment.archive import arsaug_policy, autoaug_policy, autoaug_paper_cifar10, fa_reduced_cifar10, fa_reduced_svhn, fa_resnet50_rimagenet
from FastAutoAugment.augmentations import *
from FastAutoAugment.common import get_logger
from FastAutoAugment.imagenet import ImageNet
from FastAutoAugment.networks.efficientnet_pytorch.model import EfficientNet


def __call__(self, img):
    (original_width, original_height) = img.size
    min_area = (self.area_range[0] * (original_width * original_height))
    max_area = (self.area_range[1] * (original_width * original_height))
    for _ in range(self.max_attempts):
        aspect_ratio = random.uniform(*self.aspect_ratio_range)
        height = int(round(math.sqrt((min_area / aspect_ratio))))
        max_height = int(round(math.sqrt((max_area / aspect_ratio))))
        if ((max_height * aspect_ratio) > original_width):
            max_height = (((original_width + 0.5) - 1e-07) / aspect_ratio)
            max_height = int(max_height)
            if ((max_height * aspect_ratio) > original_width):
                max_height -= 1
        if (max_height > original_height):
            max_height = original_height
        if (height >= max_height):
            height = max_height
        height = int(round(random.uniform(height, max_height)))
        width = int(round((height * aspect_ratio)))
        area = (width * height)
        if ((area < min_area) or (area > max_area)):
            continue
        if ((width > original_width) or (height > original_height)):
            continue
        if (area < (self.min_covered * (original_width * original_height))):
            continue
        if ((width == original_width) and (height == original_height)):
            return self._fallback(img)
        x = random.randint(0, (original_width - width))
        y = random.randint(0, (original_height - height))
        return img.crop((x, y, (x + width), (y + height)))
    return self._fallback(img)
