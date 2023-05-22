import torch
import torch.nn as nn
import torch.nn.functional as F
from net.utils.operation import *


def __init__(self, in_channels, out_channels, kernel_size, t_kernel_size=1, stride=1, dropout=0.5, residual=True):
    super().__init__()
    assert (len(kernel_size) == 2)
    assert ((kernel_size[0] % 2) == 1)
    padding = (((kernel_size[0] - 1) // 2), 0)
    self.gcn = SpatialConv(in_channels, out_channels, kernel_size[1], t_kernel_size)
    self.tcn = nn.Sequential(nn.BatchNorm2d(out_channels), nn.ReLU(inplace=True), nn.Conv2d(out_channels, out_channels, (kernel_size[0], 1), (stride, 1), padding), nn.BatchNorm2d(out_channels), nn.Dropout(dropout, inplace=True))
    if (not residual):
        self.residual = (lambda x: 0)
    elif ((in_channels == out_channels) and (stride == 1)):
        self.residual = (lambda x: x)
    else:
        self.residual = nn.Sequential(nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=(stride, 1)), nn.BatchNorm2d(out_channels))
    self.relu = nn.ReLU(inplace=True)
