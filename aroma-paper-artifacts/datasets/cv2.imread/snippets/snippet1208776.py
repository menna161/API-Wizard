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


def pull_item(self, index):
    img_id = self.ids[index]
    target = ET.parse((self._annopath % img_id)).getroot()
    img = cv2.imread((self._imgpath % img_id))
    (height, width, channels) = img.shape
    if (self.target_transform is not None):
        target = self.target_transform(target, width, height)
    if (self.transform is not None):
        target = np.array(target)
        (img, boxes, labels) = self.transform(img, target[(:, :4)], target[(:, 4)])
        img = img[(:, :, (2, 1, 0))]
        target = np.hstack((boxes, np.expand_dims(labels, axis=1)))
    return (torch.from_numpy(img).permute(2, 0, 1), target, height, width)
