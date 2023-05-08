import os.path as osp
import sys
import torch
import torch.utils.data as data
import cv2
import numpy as np
import xml.etree.cElementTree as ET
import xml.etree.ElementTree as ET


def __getitem__(self, index):
    img_id = self.ids[index]
    target = ET.parse((self._annopath % img_id)).getroot()
    img = cv2.imread((self._imgpath % img_id))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = (img.astype(np.float32) / 255.0)
    (height, width, channels) = img.shape
    if (self.target_transform is not None):
        target = self.target_transform(target, width, height)
    target = np.array(target)
    sample = {'img': img, 'annot': target}
    if (self.transform is not None):
        sample = self.transform(sample)
    return sample
    bbox = target[(:, :4)]
    labels = target[(:, 4)]
    if (self.transform is not None):
        annotation = {'image': img, 'bboxes': bbox, 'category_id': labels}
        augmentation = self.transform(**annotation)
        img = augmentation['image']
        bbox = augmentation['bboxes']
        labels = augmentation['category_id']
    return {'image': img, 'bboxes': bbox, 'category_id': labels}
