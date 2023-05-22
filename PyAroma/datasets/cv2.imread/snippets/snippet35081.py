import os
import cv2
import paddle.fluid as fluid
import numpy as np
import pickle
from .datasetbase import DatasetBase


def train(self, batch_size=None):
    pos_infos = self.img_infos[:int((len(self.img_infos) / 2))]
    neg_infos = self.img_infos[int((len(self.img_infos) / 2)):]
    assert (len(pos_infos) == len(neg_infos))

    def reader():
        np.random.shuffle(pos_infos)
        np.random.shuffle(neg_infos)
        img_infos = []
        for i in range(len(pos_infos)):
            img_infos.append(pos_infos[i])
            img_infos.append(neg_infos[i])
        batch = []
        for img_info in img_infos:
            img_path = os.path.join(self.img_prefix, img_info['filename'], img_info['frame'])
            label = img_info['label']
            label = (0 if (label > 1) else 1)
            img = cv2.imread(img_path)
            img = img.astype(np.float32)
            mask = np.zeros_like(img)
            (img, mask, label) = self.extra_aug(img, mask=mask, label=label)
            flip = (True if (np.random.rand() < 0.5) else False)
            (img, mask) = self.img_transform(img, self.img_scale, mask=mask, flip=flip)
            if (batch_size is None):
                (yield (img, mask, label))
            else:
                batch.append([img, mask, label])
                if (len(batch) == batch_size):
                    (yield batch)
                    batch = []
    return reader
