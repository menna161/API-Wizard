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


def __init__(self, kernel_size, dw):
    super(ShuffleConv, self).__init__()
    if dw:
        self.conv1 = nn.Sequential(depthwise(256, kernel_size), pointwise(256, 256))
        self.conv2 = nn.Sequential(depthwise(64, kernel_size), pointwise(64, 64))
        self.conv3 = nn.Sequential(depthwise(16, kernel_size), pointwise(16, 16))
        self.conv4 = nn.Sequential(depthwise(4, kernel_size), pointwise(4, 4))
    else:
        self.conv1 = conv(256, 256, kernel_size)
        self.conv2 = conv(64, 64, kernel_size)
        self.conv3 = conv(16, 16, kernel_size)
        self.conv4 = conv(4, 4, kernel_size)
