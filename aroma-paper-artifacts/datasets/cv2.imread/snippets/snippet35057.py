import os
import cv2
import numpy as np
import pickle
from .datasetbase import DatasetBase


def test(self):

    def reader():
        for img_info in self.img_infos:
            img_path = os.path.join(self.img_prefix, img_info['filename'], 'profile', img_info['frames'][(- 1)])
            label = img_info['labels'][(- 1)]
            img = cv2.imread(img_path)
            img = self.img_transform(img, self.img_scale)
            (yield (img, label))
    return reader
