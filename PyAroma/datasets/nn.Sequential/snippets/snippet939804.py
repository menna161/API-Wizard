import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import Parameter
from collections import OrderedDict


def __init__(self, in_channels, key_channels):
    super(PixelAttentionBlock_, self).__init__()
    self.in_channels = in_channels
    self.key_channels = key_channels
    self.f_key = nn.Sequential(OrderedDict([('conv', nn.Conv2d(in_channels, key_channels, kernel_size=1, stride=1, padding=0)), ('bn', nn.BatchNorm2d(key_channels)), ('relu', nn.ReLU(True))]))
    self.parameter_initialization()
    self.f_query = self.f_key
