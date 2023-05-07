import os
import math
import time
import datetime
from functools import reduce
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy.misc as misc
import torch
import torch.optim as optim
import torch.optim.lr_scheduler as lrs


def calc_psnr(sr, hr, scale, rgb_range, benchmark=False):
    diff = (sr - hr).data.div(rgb_range)
    if benchmark:
        shave = scale
        if (diff.size(1) > 1):
            convert = diff.new(1, 3, 1, 1)
            convert[(0, 0, 0, 0)] = 65.738
            convert[(0, 1, 0, 0)] = 129.057
            convert[(0, 2, 0, 0)] = 25.064
            diff.mul_(convert).div_(256)
            diff = diff.sum(dim=1, keepdim=True)
    else:
        shave = (scale + 6)
    valid = diff[(:, :, shave:(- shave), shave:(- shave))]
    mse = valid.pow(2).mean()
    return ((- 10) * math.log10(mse))
