import os
import cv2
import paddle.fluid as fluid
import numpy as np
from .transforms import ImageTransform, ExtraAugmentation


def reader():
    for img_info in self.img_infos:
        img_path = img_info['img_path']
        label = img_info['label']
        img = cv2.imread(img_path)
        img = self.img_transform(img, self.img_scale)
        (yield (img, label))
