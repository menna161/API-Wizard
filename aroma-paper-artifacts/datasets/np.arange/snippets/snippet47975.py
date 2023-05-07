import torch
import random
import cv2
import collections
import numpy as np
from skimage.filters import gaussian
from scipy.ndimage import zoom as scizoom
import torchvision.transforms as transforms


def zoom_blur(x, severity=1, patch_size=32):

    def clipped_zoom(img, zoom_factor):
        h = img.shape[0]
        ch = int(np.ceil((h / zoom_factor)))
        top = ((h - ch) // 2)
        img = scizoom(img[(top:(top + ch), top:(top + ch))], (zoom_factor, zoom_factor, 1), order=1)
        trim_top = ((img.shape[0] - h) // 2)
        return img[(trim_top:(trim_top + h), trim_top:(trim_top + h))]
    c = [np.arange(1, 1.06, 0.01), np.arange(1, 1.11, 0.01), np.arange(1, 1.16, 0.01), np.arange(1, 1.21, 0.01), np.arange(1, 1.26, 0.01)][(severity - 1)]
    x = (np.array(x) / 255.0).astype(np.float32)
    out = np.zeros_like(x)
    for zoom_factor in c:
        out += clipped_zoom(x, zoom_factor)
    x = ((x + out) / (len(c) + 1))
    return (np.clip(x, 0, 1) * 255)
