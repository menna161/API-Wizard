import os
import sys
import warnings
import cv2
import copy
import math
import numpy as np
import random
import torch
import pickle as pkl
import logging
from tqdm import tqdm
from collections import defaultdict
from PIL import Image
from logging.handlers import TimedRotatingFileHandler
import torchvision.transforms as transforms
from torch.utils.data import Sampler
from torch.utils.data import Dataset


def handle_numpy(self, img):
    '\n        img为未归一化的(H,W,C)，为albumentation使用\n        :param img:\n        :return:\n        '
    shape = img.shape
    if (random.uniform(0, 1) >= self.probability):
        return img
    for _ in range(100):
        area = (shape[0] * shape[1])
        target_area = (random.uniform(self.sl, self.sh) * area)
        aspect_ratio = random.uniform(self.r1, (1 / self.r1))
        h = int(round(math.sqrt((target_area * aspect_ratio))))
        w = int(round(math.sqrt((target_area / aspect_ratio))))
        if ((w < shape[1]) and (h < shape[0])):
            x1 = random.randint(0, (shape[0] - h))
            y1 = random.randint(0, (shape[1] - w))
            if (shape[2] == 3):
                img[x1:(x1 + h), y1:(y1 + w), 0] = (self.mean[0] * 255)
                img[x1:(x1 + h), y1:(y1 + w), 1] = (self.mean[1] * 255)
                img[x1:(x1 + h), y1:(y1 + w), 2] = (self.mean[2] * 255)
            else:
                img[x1:(x1 + h), y1:(y1 + w), 0] = self.mean[0]
            return img
    return img
