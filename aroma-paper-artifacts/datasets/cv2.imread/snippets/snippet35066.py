import os
import cv2
import paddle.fluid as fluid
import numpy as np
from .transforms import ImageTransform, ExtraAugmentation


def reader():
    batch = []
    for img_info in self.img_infos:
        img_path = img_info['img_path']
        label = img_info['label']
        img = cv2.imread(img_path)
        (img, label) = self.extra_aug(img, label=label)
        flip = (True if (np.random.rand() < 0.5) else False)
        img = self.img_transform(img, self.img_scale, flip=flip)
        if (batch_size is None):
            (yield (img, label))
        else:
            batch.append([img, label])
            if (len(batch) == batch_size):
                (yield batch)
                batch = []
