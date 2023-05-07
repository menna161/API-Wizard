from __future__ import absolute_import
import torch.nn as nn
from pytorch_benchmarks.models.model import Model


def __init__(self, num_input_channels, num_filters, stride, dim_match, bottle_neck):
    "Number of outut channels is always 'num_filters'."
    super(ResnetModule, self).__init__()
    if dim_match:
        self.shortcut = None
    else:
        self.shortcut = nn.Sequential(nn.Conv2d(num_input_channels, num_filters, kernel_size=1, stride=stride, bias=False), nn.BatchNorm2d(num_filters, eps=2e-05, momentum=0.9, affine=True))
    if bottle_neck:
        bottleneck_channels = (num_filters // 4)
        self.main = nn.Sequential(nn.Conv2d(num_input_channels, bottleneck_channels, kernel_size=1, stride=1, padding=0, bias=False), nn.BatchNorm2d(bottleneck_channels, eps=2e-05, momentum=0.9, affine=True), nn.ReLU(inplace=True), nn.Conv2d(bottleneck_channels, bottleneck_channels, kernel_size=3, stride=stride, padding=1, bias=False), nn.BatchNorm2d(bottleneck_channels, eps=2e-05, momentum=0.9, affine=True), nn.ReLU(inplace=True), nn.Conv2d(bottleneck_channels, num_filters, kernel_size=1, stride=1, padding=0, bias=False), nn.BatchNorm2d(num_filters, eps=2e-05, momentum=0.9, affine=True))
    else:
        self.main = nn.Sequential(nn.Conv2d(num_input_channels, num_filters, kernel_size=3, stride=stride, padding=1, bias=False), nn.BatchNorm2d(num_filters, eps=2e-05, momentum=0.9, affine=True), nn.ReLU(inplace=True), nn.Conv2d(num_filters, num_filters, kernel_size=3, stride=1, padding=1, bias=False), nn.BatchNorm2d(num_filters, eps=2e-05, momentum=0.9, affine=True))
    self.relu = nn.ReLU(inplace=True)
