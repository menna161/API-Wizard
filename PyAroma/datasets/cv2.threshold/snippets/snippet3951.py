import cv2
import sys
import numpy as np


def watershed(src):
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    (thresh, bin_img) = cv2.threshold(gray, 0, 255, (cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU))
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernel, iterations=2)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    (ret, sure_fg) = cv2.threshold(dist_transform, (0.7 * dist_transform.max()), 255, 0)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    (ret, markers) = cv2.connectedComponents(sure_fg)
    markers = (markers + 1)
    markers[(unknown == 255)] = 0
    markers = cv2.watershed(src, markers)
    src[(markers == (- 1))] = [255, 0, 0]
    return (markers, src)
