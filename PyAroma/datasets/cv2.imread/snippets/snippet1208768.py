from __future__ import division, print_function
from .config import HOME
import os
import os.path as osp
import sys
import torch
import torch.utils.data as data
import torchvision.transforms as transforms
import cv2
import numpy as np
from pycocotools.coco import COCO


def pull_image(self, index):
    'Returns the original image object at index in PIL form\n\n        Note: not using self.__getitem__(), as any transformations passed in\n        could mess up this functionality.\n\n        Argument:\n            index (int): index of img to show\n        Return:\n            cv2 img\n        '
    img_id = self.ids[index]
    path = self.coco.loadImgs(img_id)[0]['file_name']
    return cv2.imread(osp.join(self.root, path), cv2.IMREAD_COLOR)
