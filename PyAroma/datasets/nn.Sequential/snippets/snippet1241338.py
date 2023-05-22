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


def pointwise(in_channels, out_channels):
    return nn.Sequential(nn.Conv2d(in_channels, out_channels, 1, 1, 0, bias=False), nn.BatchNorm2d(out_channels), nn.ReLU(inplace=True))
