import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from . import STNModule
import numpy as np


def __init__(self, in_channels, kernel_size, num_classes=10, use_dropout=False):
    super(BaseSVHNet, self).__init__()
    self._in_ch = in_channels
    self._ksize = kernel_size
    self.ncls = num_classes
    self.dropout = use_dropout
    self.drop_prob = 0.5
    self.stride = 1
    self.conv1 = nn.Conv2d(self._in_ch, 32, kernel_size=self._ksize, stride=self.stride, padding=1, bias=False)
    self.conv2 = nn.Conv2d(32, 32, kernel_size=self._ksize, stride=1, padding=1, bias=False)
    self.conv3 = nn.Conv2d(32, 32, kernel_size=self._ksize, stride=1, padding=1, bias=False)
    self.fc1 = nn.Linear(((32 * 4) * 4), 1024)
    self.fc2 = nn.Linear(1024, self.ncls)
