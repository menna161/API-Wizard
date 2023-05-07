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
    super(DeConv, self).__init__()
    if dw:
        self.convt1 = nn.Sequential(convt_dw(1024, kernel_size), pointwise(1024, 512))
        self.convt2 = nn.Sequential(convt_dw(512, kernel_size), pointwise(512, 256))
        self.convt3 = nn.Sequential(convt_dw(256, kernel_size), pointwise(256, 128))
        self.convt4 = nn.Sequential(convt_dw(128, kernel_size), pointwise(128, 64))
        self.convt5 = nn.Sequential(convt_dw(64, kernel_size), pointwise(64, 32))
    else:
        self.convt1 = convt(1024, 512, kernel_size)
        self.convt2 = convt(512, 256, kernel_size)
        self.convt3 = convt(256, 128, kernel_size)
        self.convt4 = convt(128, 64, kernel_size)
        self.convt5 = convt(64, 32, kernel_size)
    self.convf = pointwise(32, 1)
