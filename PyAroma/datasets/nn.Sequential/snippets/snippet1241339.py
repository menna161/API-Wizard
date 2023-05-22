import os
import torch
import torch.nn as nn
import torchvision.models
import collections
import math
import torch.nn.functional as F
import imagenet.mobilenet
from collections import OrderedDict
from collections import OrderedDict
from collections import OrderedDict


def convt(in_channels, out_channels, kernel_size):
    stride = 2
    padding = ((kernel_size - 1) // 2)
    output_padding = (kernel_size % 2)
    assert (((((- 2) - (2 * padding)) + kernel_size) + output_padding) == 0), 'deconv parameters incorrect'
    return nn.Sequential(nn.ConvTranspose2d(in_channels, out_channels, kernel_size, stride, padding, output_padding, bias=False), nn.BatchNorm2d(out_channels), nn.ReLU(inplace=True))
