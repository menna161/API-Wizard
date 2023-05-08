import time
import os
import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, inChannels, outChannels, stride=1, **kwargs):
    super(_DSConv, self).__init__()
    self.conv = nn.Sequential(nn.Conv2d(inChannels, inChannels, 3, stride, 1, groups=inChannels, bias=False), nn.BatchNorm2d(inChannels), nn.ReLU(True), nn.Conv2d(inChannels, outChannels, 1, bias=False), nn.BatchNorm2d(outChannels), nn.ReLU(True))
