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


def upconv(in_channels, out_channels):
    return nn.Sequential(Unpool(2), nn.Conv2d(in_channels, out_channels, kernel_size=5, stride=1, padding=2, bias=False), nn.BatchNorm2d(out_channels), nn.ReLU())
