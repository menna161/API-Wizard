import time
import os
import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, inChannels, outChannels, kernel, stride=1, padding=0, **kwargs):
    super(_Conv2D, self).__init__()
    self.conv = nn.Sequential(nn.Conv2d(inChannels, outChannels, kernel, stride, padding, bias=False), nn.BatchNorm2d(outChannels), nn.ReLU(True))
