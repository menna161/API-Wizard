from __future__ import print_function, division
import sys
import os
import torch
import numpy as np
import random
import csv
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
from torch.utils.data.sampler import Sampler
from pycocotools.coco import COCO
import skimage.io
import skimage.transform
import skimage.color
import skimage
import cv2
from PIL import Image
from augmentation import get_augumentation


def load_image(self, image_index):
    image_info = self.coco.loadImgs(self.image_ids[image_index])[0]
    path = os.path.join(self.root_dir, 'images', self.set_name, image_info['file_name'])
    img = cv2.imread(path)
    if (len(img.shape) == 2):
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    return img
