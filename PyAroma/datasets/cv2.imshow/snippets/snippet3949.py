import cv2
import sys
import numpy as np


def drawMatches(img1, kp1, img2, kp2, matches):
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]
    out = np.zeros((max([rows1, rows2]), (cols1 + cols2), 3), dtype='uint8')
    out[(:rows1, :cols1, :)] = np.dstack([img1, img1, img1])
    out[(:rows2, cols1:(cols1 + cols2), :)] = np.dstack([img2, img2, img2])
    for mat in matches:
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx
        (x1, y1) = kp1[img1_idx].pt
        (x2, y2) = kp2[img2_idx].pt
        cv2.circle(out, (int(x1), int(y1)), 4, (255, 0, 0), 1)
        cv2.circle(out, ((int(x2) + cols1), int(y2)), 4, (255, 0, 0), 1)
        cv2.line(out, (int(x1), int(y1)), ((int(x2) + cols1), int(y2)), (255, 0, 0), 1)
    cv2.imshow('Matched Features', out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
