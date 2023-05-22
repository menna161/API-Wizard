import os
import cv2
import numpy as np
from .datasetbase import DatasetBase


def test(self):

    def reader():
        for img_info in self.img_infos:
            img_path = os.path.join(self.img_prefix, *[p for p in img_info['img_path'].split('/')[(- 2):]])
            label = img_info['label']
            img = cv2.imread(img_path)
            if self.crop_face:
                img = self._get_face(img, thr=self.crop_face)
            img = self.img_transform(img, self.img_scale)
            (yield (img, label))
    return reader
