from __future__ import division
import cv2
import numpy as np


def preprocess_images(paths, shape_r, shape_c):
    ims = np.zeros((len(paths), shape_r, shape_c, 3))
    for (i, path) in enumerate(paths):
        original_image = cv2.imread(path)
        padded_image = padding(original_image, shape_r, shape_c, 3)
        ims[i] = padded_image
    ims[(:, :, :, 0)] -= 103.939
    ims[(:, :, :, 1)] -= 116.779
    ims[(:, :, :, 2)] -= 123.68
    ims = ims.transpose((0, 3, 1, 2))
    return ims
