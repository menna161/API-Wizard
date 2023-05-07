import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F


def make_circle_masks(n, h, w):
    x = np.linspace((- 1.0), 1.0, w)[(None, None, :)]
    y = np.linspace((- 1.0), 1.0, h)[(None, :, None)]
    center = ((np.random.random([2, n, 1, 1]) * 1.0) - 0.5)
    r = ((np.random.random([n, 1, 1]) * 0.3) + 0.1)
    (x, y) = (((x - center[0]) / r), ((y - center[1]) / r))
    mask = (((x * x) + (y * y)) < 1.0).astype(np.float32)
    return mask
