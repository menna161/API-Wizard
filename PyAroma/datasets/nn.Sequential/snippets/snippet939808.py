import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import Parameter
from collections import OrderedDict


def __init__(self, in_channels, key_channels, value_channels, scale=1):
    super(SelfAttentionBlock_, self).__init__(in_channels, key_channels)
    self.scale = scale
    self.value_channels = value_channels
    if (scale > 1):
        self.pool = nn.MaxPool2d(kernel_size=(scale, scale))
    kernel_size = 3
    self.f_value = nn.Sequential(OrderedDict([('conv1', nn.Conv2d(in_channels, value_channels, kernel_size=kernel_size, stride=1, padding=(kernel_size // 2))), ('relu1', nn.ReLU(inplace=True)), ('conv2', nn.Conv2d(value_channels, value_channels, kernel_size=1, stride=1)), ('relu2', nn.ReLU(inplace=True))]))
    self.parameter_initialization()
