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
    sample = {}
    image_path = os.path.join(self.root_path, self.metas[idx]['image_path'])
    sample['image'] = cv2.imread(image_path)
    sample['vehicle_id'] = self.metas[idx]['vehicle_id']
    sample['color'] = int(self.metas[idx]['color'])
    sample['type'] = int(self.metas[idx]['type'])
    (origin_h, origin_w, _) = sample['image'].shape
    sample['image_shape'] = [origin_h, origin_w]
    if self.use_crop_box:
        sample = self.crop_box(sample, self.metas[idx])
    if self.use_background_substitution:
        sample = self.background_substitution(sample, self.metas[idx])
    del sample['image_shape']
    if self.transform:
        sample['image'] = self.transform(sample['image'])
    return sample
