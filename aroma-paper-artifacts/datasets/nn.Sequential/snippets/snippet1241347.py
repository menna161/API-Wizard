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


def __init__(self, in_channels, out_channels):
    super(upproj, self).__init__()
    self.unpool = Unpool(2)
    self.branch1 = nn.Sequential(nn.Conv2d(in_channels, out_channels, kernel_size=5, stride=1, padding=2, bias=False), nn.BatchNorm2d(out_channels), nn.ReLU(inplace=True), nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False), nn.BatchNorm2d(out_channels))
    self.branch2 = nn.Sequential(nn.Conv2d(in_channels, out_channels, kernel_size=5, stride=1, padding=2, bias=False), nn.BatchNorm2d(out_channels))
