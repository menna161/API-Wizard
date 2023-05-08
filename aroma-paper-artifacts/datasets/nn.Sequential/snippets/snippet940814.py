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


def __init__(self, in_channels, out_channels, kernel_size_lst, stride=2):
    super(PreprocBlock, self).__init__()
    assert ((len(kernel_size_lst) == 4) and ((out_channels % 4) == 0))
    self.lst = nn.ModuleList([])
    for (h, w) in kernel_size_lst:
        padding = ((h // 2), (w // 2))
        tmp = nn.Sequential(nn.Conv2d(in_channels, (out_channels // 4), kernel_size=(h, w), stride=stride, padding=padding), nn.BatchNorm2d((out_channels // 4)), nn.ReLU(inplace=True))
        self.lst.append(tmp)
