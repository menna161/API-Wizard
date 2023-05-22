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


def __init__(self, in_channels, out_channels=None, padding=None):
    super(UpProj.UpProjModule, self).__init__()
    if (out_channels is None):
        out_channels = (in_channels // 2)
    self.pad_3 = padding(1)
    self.pad_5 = padding(2)
    self.unpool = Unpool(in_channels)
    self.upper_branch = nn.Sequential(collections.OrderedDict([('pad1', CustomPad(self.pad_5)), ('conv1', nn.Conv2d(in_channels, out_channels, kernel_size=5, stride=1, padding=0, bias=False)), ('batchnorm1', nn.BatchNorm2d(out_channels)), ('relu', nn.ReLU()), ('pad2', CustomPad(self.pad_3)), ('conv2', nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=0, bias=False)), ('batchnorm2', nn.BatchNorm2d(out_channels))]))
    self.bottom_branch = nn.Sequential(collections.OrderedDict([('pad', CustomPad(self.pad_5)), ('conv', nn.Conv2d(in_channels, out_channels, kernel_size=5, stride=1, padding=0, bias=False)), ('batchnorm', nn.BatchNorm2d(out_channels))]))
    self.relu = nn.ReLU()
