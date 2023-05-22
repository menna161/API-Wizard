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


def pull_item(self, index):
    '\n        Args:\n            index (int): Index\n        Returns:\n            tuple: Tuple (image, target, height, width).\n                   target is the object returned by ``coco.loadAnns``.\n        '
    img_id = self.ids[index]
    target = self.coco.imgToAnns[img_id]
    ann_ids = self.coco.getAnnIds(imgIds=img_id)
    target = self.coco.loadAnns(ann_ids)
    path = osp.join(self.root, self.coco.loadImgs(img_id)[0]['file_name'])
    assert osp.exists(path), 'Image path does not exist: {}'.format(path)
    img = cv2.imread(osp.join(self.root, path))
    (height, width, _) = img.shape
    if (self.target_transform is not None):
        target = self.target_transform(target, width, height)
    if (self.transform is not None):
        target = np.array(target)
        (img, boxes, labels) = self.transform(img, target[(:, :4)], target[(:, 4)])
        img = img[(:, :, (2, 1, 0))]
        target = np.hstack((boxes, np.expand_dims(labels, axis=1)))
    return (torch.from_numpy(img).permute(2, 0, 1), target, height, width)
