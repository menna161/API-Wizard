import torch
import torch.nn as nn


def __init__(self, in_channels, growth_rate):
    super().__init__()
    inner_channel = (4 * growth_rate)
    self.bottle_neck = nn.Sequential(nn.BatchNorm2d(in_channels), nn.ReLU(inplace=True), nn.Conv2d(in_channels, inner_channel, kernel_size=1, bias=False), nn.BatchNorm2d(inner_channel), nn.ReLU(inplace=True), nn.Conv2d(inner_channel, growth_rate, kernel_size=3, padding=1, bias=False))
