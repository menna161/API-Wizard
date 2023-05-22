import torch.nn as nn
import torch
import numpy as np
import flops_benchmark


def __init__(self, first_block, channel_number, inp, oup, stride, expand_ratio):
    super(InvertedResidual, self).__init__()
    assert (stride in [1, 2])
    self.identity = ((stride == 1) and (inp == oup))
    if first_block:
        self.identity = False
    if (expand_ratio == 1):
        hidden_dim = inp
        self.conv = nn.Sequential(nn.Conv2d(inp, hidden_dim, 3, stride, 1, groups=hidden_dim, bias=False), nn.BatchNorm2d(hidden_dim), nn.ReLU6(inplace=True), nn.Conv2d(hidden_dim, oup, 1, 1, 0, bias=False), nn.BatchNorm2d(oup))
    else:
        hidden_dim = channel_number.pop(0)
        self.conv = nn.Sequential(nn.Conv2d(inp, hidden_dim, 1, 1, 0, bias=False), nn.BatchNorm2d(hidden_dim), nn.ReLU6(inplace=True), nn.Conv2d(hidden_dim, hidden_dim, 3, stride, 1, groups=hidden_dim, bias=False), nn.BatchNorm2d(hidden_dim), nn.ReLU6(inplace=True), nn.Conv2d(hidden_dim, oup, 1, 1, 0, bias=False), nn.BatchNorm2d(oup))
