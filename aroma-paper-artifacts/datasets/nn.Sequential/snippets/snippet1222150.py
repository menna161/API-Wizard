import time
import os
import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, ph1InChannel, ph2InChannel, outChannels, scale=4, **kwargs):
    super(FeatureFusion, self).__init__()
    self.scale = scale
    self.dwconv = _DWConv(ph2InChannel, outChannels, 1)
    self.upBranch = nn.Sequential(nn.Conv2d(outChannels, outChannels, 1), nn.BatchNorm2d(outChannels))
    self.downBranch = nn.Sequential(nn.Conv2d(ph1InChannel, outChannels, 1), nn.BatchNorm2d(outChannels))
    self.activation = nn.ReLU(True)
