import os
import cv2
import numpy as np
import pickle
from .datasetbase import DatasetBase


def train(self, batch_size=None):
    np.random.shuffle(self.img_infos)

    def reader():
        batch = []
        for img_info in self.img_infos:
            img_path = os.path.join(self.img_prefix, img_info['filename'], 'profile', img_info['frames'][0])
            label = img_info['labels'][0]
            img = cv2.imread(img_path)
            img = img.astype(np.float32)
            mask = np.zeros_like(img)
            (img, mask, label) = self.extra_aug(img, mask=mask, label=label)
            flip = (True if (np.random.rand() < 0.5) else False)
            img = self.img_transform(img, self.img_scale, flip=flip)
            if (batch_size is None):
                (yield (img, label))
            else:
                batch.append([img, label])
                if (len(batch) == batch_size):
                    (yield batch)
                    batch = []
    return reader
