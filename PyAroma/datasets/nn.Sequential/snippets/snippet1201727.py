from collections import OrderedDict
import math
import torch
import torch.nn as nn
from torch.utils import model_zoo
from torch.nn import BatchNorm2d


def __init__(self, channels, reduction=16, mode='concat'):
    super(SCSEModule, self).__init__()
    self.avg_pool = nn.AdaptiveAvgPool2d(1)
    self.fc1 = nn.Conv2d(channels, (channels // reduction), kernel_size=1, padding=0)
    self.relu = nn.ReLU(inplace=True)
    self.fc2 = nn.Conv2d((channels // reduction), channels, kernel_size=1, padding=0)
    self.sigmoid = nn.Sigmoid()
    self.spatial_se = nn.Sequential(nn.Conv2d(channels, 1, kernel_size=1, stride=1, padding=0, bias=False), nn.Sigmoid())
    self.mode = mode
