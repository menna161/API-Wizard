from __future__ import absolute_import
import torch
import torch.nn as nn
from pytorch_benchmarks.models.model import Model


def __init__(self, num_input_channels, num_1x1, num_3x3red, num_3x3, num_d5x5red, num_d5x5, proj):
    super(InceptionModule, self).__init__()
    self.conv1 = ConvModule(num_input_channels, num_filters=num_1x1, kernel_size=1)
    self.conv3 = nn.Sequential(ConvModule(num_input_channels, num_filters=num_3x3red, kernel_size=1), ConvModule(num_3x3red, num_filters=num_3x3, kernel_size=3, padding=1))
    self.conv5 = nn.Sequential(ConvModule(num_input_channels, num_filters=num_d5x5red, kernel_size=1), ConvModule(num_d5x5red, num_filters=num_d5x5, kernel_size=5, padding=2))
    self.pooling = nn.Sequential(nn.MaxPool2d(kernel_size=3, stride=1, padding=1), ConvModule(num_input_channels, num_filters=proj, kernel_size=1))
