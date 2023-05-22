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


def pull_item(self, index):
    target = self.label_ids[index]
    img = cv2.imread(self.img_ids[index])
    (height, width, channels) = img.shape
    if (self.target_transform is not None):
        target = self.target_transform(target, width, height)
    if (self.transform is not None):
        target = np.array(target)
        (img, boxes, labels) = self.transform(img, target[(:, :4)], target[(:, 4)])
        target = np.hstack((boxes, np.expand_dims(labels, axis=1)))
    return (torch.from_numpy(img).permute(2, 0, 1), target, height, width)
