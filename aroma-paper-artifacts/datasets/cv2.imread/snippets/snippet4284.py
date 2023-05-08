import cv2
import os
import numpy as np
import torch
from torch.utils.data import Dataset


def __getitem__(self, idx):
    img = cv2.imread(self.img_list[idx])
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if (self.image_set != 'test'):
        segLabel = cv2.imread(self.segLabel_list[idx])[(:, :, 0)]
        exist = np.array(self.exist_list[idx])
    else:
        segLabel = None
        exist = None
    sample = {'img': img, 'segLabel': segLabel, 'exist': exist, 'img_name': self.img_list[idx]}
    if (self.transforms is not None):
        sample = self.transforms(sample)
    return sample
