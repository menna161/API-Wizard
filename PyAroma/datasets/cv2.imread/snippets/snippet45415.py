from .config import HOME
import os.path as osp
import sys
import torch
import torch.utils.data as data
import cv2
import numpy as np
from gtdb import box_utils
from gtdb import feature_extractor
import copy
import utils.visualize as visualize


def read_all_images(self):
    for id in self.ids:
        image = cv2.imread((self._imgpath % id), cv2.IMREAD_COLOR)
        self.images[id[1]] = image
