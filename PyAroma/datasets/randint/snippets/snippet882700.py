import os, sys
import numpy as np
import torch
from utility.utils import device


def rand_bbox(self, size, lam):
    W = size[2]
    H = size[3]
    cut_rat = np.sqrt((1.0 - lam))
    cut_w = np.int((W * cut_rat))
    cut_h = np.int((H * cut_rat))
    cx = np.random.randint(W)
    cy = np.random.randint(H)
    bbx1 = np.clip((cx - (cut_w // 2)), 0, W)
    bby1 = np.clip((cy - (cut_h // 2)), 0, H)
    bbx2 = np.clip((cx + (cut_w // 2)), 0, W)
    bby2 = np.clip((cy + (cut_h // 2)), 0, H)
    return (bbx1, bby1, bbx2, bby2)