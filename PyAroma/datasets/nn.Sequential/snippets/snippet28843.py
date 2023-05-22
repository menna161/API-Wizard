import warnings
from collections import namedtuple
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils import model_zoo
import scipy.stats as stats


def __init__(self, in_channels, ch1x1, ch3x3red, ch3x3, ch5x5red, ch5x5, pool_proj):
    super(Inception, self).__init__()
    self.branch1 = BasicConv2d(in_channels, ch1x1, kernel_size=1)
    self.branch2 = nn.Sequential(BasicConv2d(in_channels, ch3x3red, kernel_size=1), BasicConv2d(ch3x3red, ch3x3, kernel_size=3, padding=1))
    self.branch3 = nn.Sequential(BasicConv2d(in_channels, ch5x5red, kernel_size=1), BasicConv2d(ch5x5red, ch5x5, kernel_size=3, padding=1))
    self.branch4 = nn.Sequential(nn.MaxPool2d(kernel_size=3, stride=1, padding=1, ceil_mode=True), BasicConv2d(in_channels, pool_proj, kernel_size=1))
