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
    super(NNConv, self).__init__()
    if dw:
        self.conv1 = nn.Sequential(depthwise(1024, kernel_size), pointwise(1024, 512))
        self.conv2 = nn.Sequential(depthwise(512, kernel_size), pointwise(512, 256))
        self.conv3 = nn.Sequential(depthwise(256, kernel_size), pointwise(256, 128))
        self.conv4 = nn.Sequential(depthwise(128, kernel_size), pointwise(128, 64))
        self.conv5 = nn.Sequential(depthwise(64, kernel_size), pointwise(64, 32))
        self.conv6 = pointwise(32, 1)
    else:
        self.conv1 = conv(1024, 512, kernel_size)
        self.conv2 = conv(512, 256, kernel_size)
        self.conv3 = conv(256, 128, kernel_size)
        self.conv4 = conv(128, 64, kernel_size)
        self.conv5 = conv(64, 32, kernel_size)
        self.conv6 = pointwise(32, 1)
