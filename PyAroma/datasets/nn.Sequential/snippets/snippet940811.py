import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models
import collections
import math
import sys
import Utils
from Utils.CubePad import CustomPad
from . import resnet
import resnet


def upconv_module(self, in_channels):
    upconv = nn.Sequential(collections.OrderedDict([('unpool', Unpool(in_channels)), ('conv', nn.Conv2d(in_channels, (in_channels // 2), kernel_size=5, stride=1, padding=2, bias=False)), ('batchnorm', nn.BatchNorm2d((in_channels // 2))), ('relu', nn.ReLU())]))
    return upconv
