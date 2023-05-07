import os
from PIL import Image
import cv2
import torch
from torch.utils import data
from torchvision import transforms
from torchvision.transforms import functional as F
import numbers
import numpy as np
import random


def cv_random_flip(img, label):
    flip_flag = random.randint(0, 1)
    if (flip_flag == 1):
        img = img[(:, :, ::(- 1))].copy()
        label = label[(:, :, ::(- 1))].copy()
    return (img, label)
