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


def depthwise(in_channels, kernel_size):
    padding = ((kernel_size - 1) // 2)
    assert ((2 * padding) == (kernel_size - 1)), 'parameters incorrect. kernel={}, padding={}'.format(kernel_size, padding)
    return nn.Sequential(nn.Conv2d(in_channels, in_channels, kernel_size, stride=1, padding=padding, bias=False, groups=in_channels), nn.BatchNorm2d(in_channels), nn.ReLU(inplace=True))
