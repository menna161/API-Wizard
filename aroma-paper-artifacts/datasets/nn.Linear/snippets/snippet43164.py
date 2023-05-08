import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from . import STNModule
import numpy as np


def __init__(self, spatial_dim, in_channels, stn_kernel_size, kernel_size, num_classes=10, use_dropout=False):
    super(STNSVHNet, self).__init__()
    self._in_ch = in_channels
    self._ksize = kernel_size
    self._sksize = stn_kernel_size
    self.ncls = num_classes
    self.dropout = use_dropout
    self.drop_prob = 0.5
    self.stride = 1
    self.spatial_dim = spatial_dim
    self.stnmod = STNModule.SpatialTransformer(self._in_ch, self.spatial_dim, self._sksize)
    self.conv1 = nn.Conv2d(self._in_ch, 32, kernel_size=self._ksize, stride=self.stride, padding=1, bias=False)
    self.conv2 = nn.Conv2d(32, 64, kernel_size=self._ksize, stride=1, padding=1, bias=False)
    self.conv3 = nn.Conv2d(64, 128, kernel_size=self._ksize, stride=1, padding=1, bias=False)
    self.fc1 = nn.Linear(((128 * 4) * 4), 3092)
    self.fc2 = nn.Linear(3092, self.ncls)
