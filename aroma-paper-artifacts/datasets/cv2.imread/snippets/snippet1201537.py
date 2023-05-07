import os
import cv2
import numpy as np
import pandas as pd
from skimage.external import tifffile
from torch.utils.data import Dataset


def __getitem__(self, idx):
    try:
        img = tifffile.imread(os.path.join(self.data_path, self.names[idx]))
    except Exception as e:
        print(os.path.join(self.data_path, self.names[idx]))
        raise e
    if (np.shape(img)[0] == 4):
        img = np.moveaxis(img, 0, (- 1))
    img = stretch_8bit(img)
    mask = cv2.imread(os.path.join('train_labels', 'masks_all', (('mask_' + '_'.join(self.names[idx][:(- 4)].split('_')[(- 2):])) + '.png')), cv2.IMREAD_COLOR)
    if (mask is None):
        mask = []
    else:
        mask = (mask / 255.0)
    nadir = nadirs['all'].index(self.names[idx].split('/')[0])
    angle = np.zeros((1, 1, 27))
    angle[(0, 0, nadir)] = 1
    sample = {'img': img, 'mask': mask, 'img_name': self.names[idx], 'angle': angle}
    if self.transform:
        sample = self.transform(sample)
    return sample
