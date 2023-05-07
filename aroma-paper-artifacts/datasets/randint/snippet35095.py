import cv2
import numpy as np


def __call__(self, img, mask=None, label=None):
    if (np.random.uniform(0, 1) < self.p):
        (h, w) = (img.shape[0], img.shape[1])
        angle = np.random.randint((- self.angle), self.angle)
        M = cv2.getRotationMatrix2D(((w / 2), (h / 2)), angle, 1)
        img = cv2.warpAffine(img, M, (w, h))
        if (mask is not None):
            mask = cv2.warpAffine(mask, M, (w, h))
    if (mask is not None):
        return (img, mask, label)
    else:
        return (img, label)
