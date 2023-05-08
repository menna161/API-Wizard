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


def get_gaussian_kernel(kernel_size=3, sigma=2, channels=3):
    x_coord = torch.arange(kernel_size)
    x_grid = x_coord.repeat(kernel_size).view(kernel_size, kernel_size)
    y_grid = x_grid.t()
    xy_grid = torch.stack([x_grid, y_grid], dim=(- 1)).float()
    mean = ((kernel_size - 1) / 2.0)
    variance = (sigma ** 2.0)
    gaussian_kernel = ((1.0 / ((2.0 * math.pi) * variance)) * torch.exp(((- torch.sum(((xy_grid - mean) ** 2.0), dim=(- 1))) / (2 * variance))))
    gaussian_kernel = (gaussian_kernel / torch.sum(gaussian_kernel))
    gaussian_kernel = gaussian_kernel.view(1, 1, kernel_size, kernel_size)
    gaussian_kernel = gaussian_kernel.repeat(channels, 1, 1, 1)
    paddingl = ((kernel_size - 1) // 2)
    paddingr = ((kernel_size - 1) - paddingl)
    pad = torch.nn.ReflectionPad2d((paddingl, paddingr, paddingl, paddingr))
    gaussian_filter = nn.Conv2d(in_channels=channels, out_channels=channels, kernel_size=kernel_size, groups=channels, bias=False)
    gaussian_filter.weight.data = gaussian_kernel
    gaussian_filter.weight.requires_grad = False
    return nn.Sequential(pad, gaussian_filter)
