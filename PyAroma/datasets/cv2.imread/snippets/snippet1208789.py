from __future__ import division, print_function
import os.path as osp
import sys
import torch
import torch.utils.data as data
import cv2
import numpy as np
import scipy.io
import pdb
from collections import defaultdict
import matplotlib.pyplot as plt


def pull_image(self, index):
    'Returns the original image object at index in PIL form\n\n        Note: not using self.__getitem__(), as any transformations passed in\n        could mess up this functionality.\n\n        Argument:\n            index (int): index of img to show\n        Return:\n            PIL img\n        '
    return cv2.imread(self.img_ids[index], cv2.IMREAD_COLOR)
