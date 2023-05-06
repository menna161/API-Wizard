import torch
import random
import cv2
import collections
import numpy as np
from skimage.filters import gaussian
from scipy.ndimage import zoom as scizoom
import torchvision.transforms as transforms


def defocus_blur(x, severity=1, patch_size=32):

    def disk(radius, alias_blur=0.1, dtype=np.float32):
        if (radius <= 8):
            L = np.arange((- 8), (8 + 1))
            ksize = (3, 3)
        else:
            L = np.arange((- radius), (radius + 1))
            ksize = (5, 5)
        (X, Y) = np.meshgrid(L, L)
        aliased_disk = np.array((((X ** 2) + (Y ** 2)) <= (radius ** 2)), dtype=dtype)
        aliased_disk /= np.sum(aliased_disk)
        return cv2.GaussianBlur(aliased_disk, ksize=ksize, sigmaX=alias_blur)
    c = [(0.3, 0.4), (0.4, 0.5), (0.5, 0.6), (1, 0.2), (1.5, 0.1)][(severity - 1)]
    x = (np.array(x) / 255.0)
    kernel = disk(radius=c[0], alias_blur=c[1])
    channels = []
    for d in range(3):
        channels.append(cv2.filter2D(x[(:, :, d)], (- 1), kernel))
    channels = np.array(channels).transpose((1, 2, 0))
    return (np.clip(channels, 0, 1) * 255)
