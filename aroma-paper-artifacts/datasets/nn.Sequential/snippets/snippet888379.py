import torch
import torch.nn as nn


def __init__(self, in_channels, out_channels):
    super().__init__()
    self.down_sample = nn.Sequential(nn.BatchNorm2d(in_channels), nn.Conv2d(in_channels, out_channels, 1, bias=False), nn.AvgPool2d(2, stride=2))
