import os, sys
import numpy as np
import torch
from utility.utils import device


def apply(self, img):
    '\n        Args:\n            img (Tensor): Tensor image of size (C, H, W).\n        Returns:\n            Tensor: Image with n_holes of dimension length x length cut out of it.\n        '
    h = img.size(2)
    w = img.size(3)
    mask = np.ones((h, w), np.float32)
    for n in range(self.n_holes):
        y = np.random.randint(h)
        x = np.random.randint(w)
        y1 = int(np.clip((y - (self.length / 2)), 0, h))
        y2 = int(np.clip((y + (self.length / 2)), 0, h))
        x1 = int(np.clip((x - (self.length / 2)), 0, w))
        x2 = int(np.clip((x + (self.length / 2)), 0, w))
        mask[(y1:y2, x1:x2)] = 0.0
    mask = torch.from_numpy(mask)
    mask = mask.expand_as(img).to(device)
    img = (img * mask)
    return img
