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


def get_empty_background(self):
    idx = np.random.randint(0, len(self.metas))
    meta = self.metas[idx]
    bg_sample = meta.copy()
    image_path = os.path.join(self.root_path, bg_sample['image_path'])
    bg_sample['image'] = cv2.imread(image_path)
    bg_sample = self.read_mask(bg_sample)
    (H, W, _) = bg_sample['mask'].shape
    mask = (bg_sample['mask'][(:, :, 0)] > 0.5)
    bg = (bg_sample['image'] * mask.reshape(H, W, 1))
    bg_avg = bg[((mask != 0), :)].mean(axis=0)
    bg_fill = (bg_avg.reshape(1, 1, 3) * (1 - mask).reshape(H, W, 1))
    bg = (bg + bg_fill)
    return bg
