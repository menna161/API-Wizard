import os
import numpy as np
from PIL import Image
import torch
from torch import nn
from torch.nn.modules.conv import _ConvNd
from torch.nn.modules.batchnorm import _BatchNorm
import torch.nn.init as initer
import torch.nn.functional as F
import socket


def mixup_data(x, y, alpha=0.2):
    'Returns mixed inputs, pairs of targets, and lambda'
    if (alpha > 0):
        lam = np.random.beta(alpha, alpha)
    else:
        lam = 1
    index = torch.randperm(x.shape[0])
    x = ((lam * x) + ((1 - lam) * x[(index, :)]))
    (y_a, y_b) = (y, y[index])
    return (x, y_a, y_b, lam)
