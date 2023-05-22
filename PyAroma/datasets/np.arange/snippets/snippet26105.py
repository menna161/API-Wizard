import random
import collections
import numpy as np
import torch
from PIL import Image, ImageOps
import cv2
import albumentations.augmentations.functional as F
import accimage


def randomize_parameters(self):
    ksize = random.choice(np.arange(self.blur_limit[0], (self.blur_limit[1] + 1), 2))
    assert (ksize > 2)
    kernel = np.zeros((ksize, ksize), dtype=np.uint8)
    (xs, xe) = (random.randint(0, (ksize - 1)), random.randint(0, (ksize - 1)))
    if (xs == xe):
        (ys, ye) = random.sample(range(ksize), 2)
    else:
        (ys, ye) = (random.randint(0, (ksize - 1)), random.randint(0, (ksize - 1)))
    cv2.line(kernel, (xs, ys), (xe, ye), 1, thickness=1)
    self.kernel = (kernel.astype(np.float32) / np.sum(kernel))
    self.apply = random.random()
