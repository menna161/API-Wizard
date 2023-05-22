import os
import cv2
import numpy as np
from .datasetbase import DatasetBase


def reader():
    np.random.shuffle(pos_infos)
    np.random.shuffle(neg_infos)
    img_infos = []
    for i in range(len(pos_infos)):
        img_infos.append(pos_infos[i])
        img_infos.append(neg_infos[i])
    batch = []
    for img_info in img_infos:
        img_path = os.path.join(self.img_prefix, *[p for p in img_info['img_path'].split('/')[(- 7):]])
        label = img_info['label']
        img = cv2.imread(img_path)
        mask = (self._get_mask(self.kp_dict[img_info['img_path']], img) if self.with_mask else np.zeros_like(img))
        if self.crop_face:
            (img, mask) = self._get_face(img, mask, thr=self.crop_face)
        img = img.astype(np.float32)
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
