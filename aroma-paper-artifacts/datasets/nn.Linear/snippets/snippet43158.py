import os
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, in_channels, spatial_dims, kernel_size, use_dropout=False):
    super(SpatialTransformer, self).__init__()
    (self._h, self._w) = spatial_dims
    self._in_ch = in_channels
    self._ksize = kernel_size
    self.dropout = use_dropout
    self.conv1 = nn.Conv2d(in_channels, 32, kernel_size=self._ksize, stride=1, padding=1, bias=False)
    self.conv2 = nn.Conv2d(32, 32, kernel_size=self._ksize, stride=1, padding=1, bias=False)
    self.conv3 = nn.Conv2d(32, 32, kernel_size=self._ksize, stride=1, padding=1, bias=False)
    self.conv4 = nn.Conv2d(32, 32, kernel_size=self._ksize, stride=1, padding=1, bias=False)
    self.fc1 = nn.Linear(((32 * 4) * 4), 1024)
    self.fc2 = nn.Linear(1024, 6)
