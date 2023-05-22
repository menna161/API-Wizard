from __future__ import division
import cv2
import numpy as np


def preprocess_maps(paths, shape_r, shape_c):
    ims = np.zeros((len(paths), 1, shape_r, shape_c))
    for (i, path) in enumerate(paths):
        original_map = cv2.imread(path, 0)
        padded_map = padding(original_map, shape_r, shape_c, 1)
        ims[(i, 0)] = padded_map.astype(np.float32)
        ims[(i, 0)] /= 255.0
    return ims
