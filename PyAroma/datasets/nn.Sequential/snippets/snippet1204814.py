from __future__ import absolute_import
import torch
import torch.nn as nn
from pytorch_benchmarks.models.model import Model


def __init__(self, num_input_channels, num_filters, kernel_size, stride=1, padding=0):
    super(ConvModule, self).__init__()
    self.conv_module = nn.Sequential(nn.Conv2d(num_input_channels, num_filters, kernel_size=kernel_size, stride=stride, padding=padding), nn.BatchNorm2d(num_filters, eps=2e-05, momentum=0.9, affine=True), nn.ReLU(inplace=True))
