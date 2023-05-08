import os
import cv2
import paddle.fluid as fluid
import numpy as np
import pickle
from .datasetbase import DatasetBase


def test(self):

    def reader():
        for img_info in self.img_infos:
            img_path = os.path.join(self.img_prefix, img_info['filename'], img_info['frame'])
            label = img_info['label']
            label = (0 if (label > 1) else 1)
            img = cv2.imread(img_path)
            img = self.img_transform(img, self.img_scale)
            (yield (img, label))
    return reader
