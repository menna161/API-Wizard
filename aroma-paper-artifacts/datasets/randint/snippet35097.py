import cv2
import numpy as np


def __call__(self, img, mask=None, label=None):
    if (np.random.uniform(0, 1) < self.p):
        (h, w) = (img.shape[0], img.shape[1])
        (_w, _h) = self.w_h
        x1 = np.random.randint(0, int((_w * w)))
        y1 = np.random.randint(0, int((_h * h)))
        x2 = np.random.randint(int(((1 - _w) * w)), w)
        y2 = np.random.randint(int(((1 - _h) * h)), h)
        img = img[(y1:y2, x1:x2, :)]
        if (mask is not None):
            mask = mask[(y1:y2, x1:x2, :)]
    if (mask is not None):
        return (img, mask, label)
    else:
        return (img, label)
