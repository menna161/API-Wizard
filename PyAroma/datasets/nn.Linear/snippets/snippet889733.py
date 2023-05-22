import torch.nn as nn
import math


def __init__(self, channel, reduction=4):
    super(SELayer, self).__init__()
    self.avg_pool = nn.AdaptiveAvgPool2d(1)
    self.fc = nn.Sequential(nn.Linear(channel, _make_divisible((channel // reduction), 8)), nn.ReLU(inplace=True), nn.Linear(_make_divisible((channel // reduction), 8), channel), h_sigmoid())
