import torch
import random
import cv2
import collections
import numpy as np
from skimage.filters import gaussian
from scipy.ndimage import zoom as scizoom
import torchvision.transforms as transforms


def glass_blur(x, severity=1, patch_size=32):
    c = [(0.05, 1, 1), (0.25, 1, 1), (0.4, 1, 1), (0.25, 1, 2), (0.4, 1, 2)][(severity - 1)]
    x = np.uint8((gaussian((np.array(x) / 255.0), sigma=c[0], multichannel=True) * 255))
    for i in range(c[2]):
        for h in range((patch_size - c[1]), c[1], (- 1)):
            for w in range((patch_size - c[1]), c[1], (- 1)):
                (dx, dy) = np.random.randint((- c[1]), c[1], size=(2,))
                (h_prime, w_prime) = ((h + dy), (w + dx))
                (x[(h, w)], x[(h_prime, w_prime)]) = (x[(h_prime, w_prime)], x[(h, w)])
    return (np.clip(gaussian((x / 255.0), sigma=c[0], multichannel=True), 0, 1) * 255)
