import cv2
import numpy as np


def getLane_CULane(prob_map, y_px_gap, pts, thresh, resize_shape=None):
    '\n    Arguments:\n    ----------\n    prob_map: prob map for single lane, np array size (h, w)\n    resize_shape:  reshape size target, (H, W)\n    Return:\n    ----------\n    coords: x coords bottom up every y_px_gap px, 0 for non-exist, in resized shape\n    '
    if (resize_shape is None):
        resize_shape = prob_map.shape
    (h, w) = prob_map.shape
    (H, W) = resize_shape
    coords = np.zeros(pts)
    for i in range(pts):
        y = int(((h - (((i * y_px_gap) / H) * h)) - 1))
        if (y < 0):
            break
        line = prob_map[(y, :)]
        id = np.argmax(line)
        if (line[id] > thresh):
            coords[i] = int(((id / w) * W))
    if ((coords > 0).sum() < 2):
        coords = np.zeros(pts)
    return coords
