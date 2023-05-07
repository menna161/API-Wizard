import torch
import torch.nn as nn
from torch.nn import init
import functools
from torch.optim import lr_scheduler
from .vgg import Vgg19
import math
import cv2
import numpy as np
import scipy.stats as st
import code


def gkern(kernlen=100, nsig=1):
    'Returns a 2D Gaussian kernel array.'
    interval = (((2 * nsig) + 1.0) / kernlen)
    x = np.linspace(((- nsig) - (interval / 2.0)), (nsig + (interval / 2.0)), (kernlen + 1))
    kern1d = np.diff(st.norm.cdf(x))
    kernel_raw = np.sqrt(np.outer(kern1d, kern1d))
    kernel = (kernel_raw / kernel_raw.sum())
    kernel = (kernel / kernel.max())
    return kernel
