import time
import os
import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, inChannels, outChannels, t=6, stride=2, **kwargs):
    super(_Bottleneck, self).__init__()
    self.shortcut = ((stride == 1) and (inChannels == outChannels))
    self.block = nn.Sequential(_Conv2D(inChannels, (inChannels * t), 1), _DWConv((inChannels * t), (inChannels * t), stride), nn.Conv2d((inChannels * t), outChannels, 1, bias=False), nn.BatchNorm2d(outChannels))
