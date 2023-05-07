from __future__ import division
import pdb
from .config import HOME
import os.path as osp
import sys
import torch
import torch.utils.data as data
import cv2
import numpy as np
import xml.etree.cElementTree as ET
import xml.etree.ElementTree as ET


def pull_image(self, index):
    'Returns the original image object at index in PIL form\n\n        Note: not using self.__getitem__(), as any transformations passed in\n        could mess up this functionality.\n\n        Argument:\n            index (int): index of img to show\n        Return:\n            PIL img\n        '
    img_id = self.ids[index]
    return cv2.imread((self._imgpath % img_id), cv2.IMREAD_COLOR)
