import cv2
import math
import numpy as np
import torch
import transforms3d


def __call__(self, img):
    (img_h, img_w, img_c) = img.shape
    if (not (img_c == 4)):
        return img
    (r, g, b) = [np.random.randint(self.random_bg_color_range[i][0], (self.random_bg_color_range[i][1] + 1)) for i in range(3)]
    alpha = (np.expand_dims(img[(:, :, 3)], axis=2) == 0).astype(np.float32)
    img = img[(:, :, :3)]
    bg_color = (np.array([[[r, g, b]]]) / 255.0)
    img = ((alpha * bg_color) + ((1 - alpha) * img))
    return img
