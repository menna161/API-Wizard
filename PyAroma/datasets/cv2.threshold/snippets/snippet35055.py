import os
import cv2
import numpy as np
import pickle
from .datasetbase import DatasetBase


def _get_mask(self, img, thr=10, crop=False):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (_, mask) = cv2.threshold(gray, thr, 1, cv2.THRESH_BINARY)
    (indy, indx) = np.where((mask > 0))
    (x1, y1) = (indx.min(), indy.min())
    (x2, y2) = (indx.max(), indy.max())
    y1 = int(((y1 + y2) / 2))
    if crop:
        return (img[(y1:y2, x1:x2, :)], mask[(y1:y2, x1:x2)])
    else:
        return (img, mask)
