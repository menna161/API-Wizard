import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from dropblock import DropBlock2D


def __init__(self, in_ch, out_ch, group_conv, dilation=1):
    super(double_conv, self).__init__()
    if group_conv:
        self.conv = nn.Sequential(nn.Conv2d(in_ch, out_ch, 3, padding=1, groups=min(out_ch, in_ch)), nn.BatchNorm2d(out_ch), nn.LeakyReLU(inplace=True), nn.Conv2d(out_ch, out_ch, 3, padding=1, groups=out_ch), nn.BatchNorm2d(out_ch), nn.LeakyReLU(inplace=True))
    else:
        self.conv = nn.Sequential(nn.Conv2d(in_ch, out_ch, 3, padding=1), nn.BatchNorm2d(out_ch), nn.LeakyReLU(inplace=True), nn.Conv2d(out_ch, out_ch, 3, padding=1), nn.BatchNorm2d(out_ch), nn.LeakyReLU(inplace=True))
