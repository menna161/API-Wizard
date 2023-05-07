import cv2
import numpy as np


def __call__(self, img, mask=None, label=None):
    if np.random.randint(2):
        delta = np.random.uniform((- self.bd), self.bd)
        img += delta
    if np.random.randint(2):
        alpha = np.random.uniform(self.cl, self.ch)
        img *= alpha
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    if np.random.randint(2):
        img[(..., 1)] *= np.random.uniform(self.sl, self.sh)
    if np.random.randint(2):
        img[(..., 0)] += np.random.uniform((- self.hd), self.hd)
        img[(..., 0)][(img[(..., 0)] > 360)] -= 360
        img[(..., 0)][(img[(..., 0)] < 0)] += 360
    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    if (mask is not None):
        return (img, mask, label)
    else:
        return (img, label)
