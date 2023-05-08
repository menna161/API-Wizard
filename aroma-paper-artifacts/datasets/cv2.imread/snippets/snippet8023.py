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


def __getitem__(self, idx):
    image_path = os.path.join(self.root_path, self.total_meta[idx]['image_path'])
    image = cv2.imread(image_path)
    if self.use_crop_box:
        image = self.crop_box(image, self.total_meta[idx])
    if self.transform:
        image = self.transform(image)
    return image
