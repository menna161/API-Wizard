from __future__ import print_function
import cv2
import numpy as np
import torch
import torch.nn as nn


def getCoords(image):
    (contours, _) = cv2.findContours(preprocess, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    all_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    polygon = all_contours[0]
    sums = []
    diffs = []
    for point in polygon:
        for (x, y) in point:
            sums.append((x + y))
            diffs.append((x - y))
    top_left = polygon[np.argmin(sums)].squeeze()
    bottom_right = polygon[np.argmax(sums)].squeeze()
    top_right = polygon[np.argmax(diffs)].squeeze()
    bottom_left = polygon[np.argmin(diffs)].squeeze()
    return np.array([top_left, top_right, bottom_right, bottom_left], dtype=np.float32)
