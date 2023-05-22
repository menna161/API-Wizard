from __future__ import division
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import init


def __init__(self, in_channels, out_channels, stride, cardinality, base_width, widen_factor):
    ' Constructor\n\n        Args:\n            in_channels: input channel dimensionality\n            out_channels: output channel dimensionality\n            stride: conv stride. Replaces pooling layer.\n            cardinality: num of convolution groups.\n            base_width: base number of channels in each group.\n            widen_factor: factor to reduce the input dimensionality before convolution.\n        '
    super(ResNeXtBottleneck, self).__init__()
    width_ratio = (out_channels / (widen_factor * 64.0))
    D = (cardinality * int((base_width * width_ratio)))
    self.conv_reduce = nn.Conv2d(in_channels, D, kernel_size=1, stride=1, padding=0, bias=False)
    self.bn_reduce = nn.BatchNorm2d(D)
    self.conv_conv = nn.Conv2d(D, D, kernel_size=3, stride=stride, padding=1, groups=cardinality, bias=False)
    self.bn = nn.BatchNorm2d(D)
    self.conv_expand = nn.Conv2d(D, out_channels, kernel_size=1, stride=1, padding=0, bias=False)
    self.bn_expand = nn.BatchNorm2d(out_channels)
    self.shortcut = nn.Sequential()
    if (in_channels != out_channels):
        self.shortcut.add_module('shortcut_conv', nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, padding=0, bias=False))
        self.shortcut.add_module('shortcut_bn', nn.BatchNorm2d(out_channels))
