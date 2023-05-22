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
    (h, w) = (img.size(1), img.size(2))
    mask = np.ones((h, w), np.float32)
    y = np.random.randint(h)
    x = np.random.randint(w)
    y1 = np.clip((y - (self.length // 2)), 0, h)
    y2 = np.clip((y + (self.length // 2)), 0, h)
    x1 = np.clip((x - (self.length // 2)), 0, w)
    x2 = np.clip((x + (self.length // 2)), 0, w)
    mask[(y1:y2, x1:x2)] = 0.0
    mask = torch.from_numpy(mask)
    mask = mask.expand_as(img)
    img *= mask
    return img
