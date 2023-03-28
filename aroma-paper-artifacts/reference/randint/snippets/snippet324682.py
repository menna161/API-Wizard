import os
import numpy as np
import torch
import shutil
import torchvision.transforms as transforms
from torch.autograd import Variable


def __call__(self, img):
    (h, w) = (img.size(1), img.size(2))
    mask = np.ones((h, w), np.float32)
    y = np.random.randint(h)
    x = np.random.randint(w)
    y1 = np.clip((y - (self.length // 2)), 0, h)
    y2 = np.clip((y + (self.length // 2)), 0, h)
    x1 = np.clip((x - (self.length // 2)), 0, w)
    x2 = np.clip((x + (self.length // 2)), 0, w)
    mask[y1:y2, x1:x2] = 0.0
    mask = torch.from_numpy(mask)
    mask = mask.expand_as(img)
    img *= mask
    return img
