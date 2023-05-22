import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, in_channels, out_channels, stride):
    super().__init__()
    self.stride = stride
    self.in_channels = in_channels
    self.out_channels = out_channels
    if ((stride != 1) or (in_channels != out_channels)):
        self.residual = nn.Sequential(nn.Conv2d(in_channels, in_channels, 1), nn.BatchNorm2d(in_channels), nn.ReLU(inplace=True), nn.Conv2d(in_channels, in_channels, 3, stride=stride, padding=1, groups=in_channels), nn.BatchNorm2d(in_channels), nn.Conv2d(in_channels, int((out_channels / 2)), 1), nn.BatchNorm2d(int((out_channels / 2))), nn.ReLU(inplace=True))
        self.shortcut = nn.Sequential(nn.Conv2d(in_channels, in_channels, 3, stride=stride, padding=1, groups=in_channels), nn.BatchNorm2d(in_channels), nn.Conv2d(in_channels, int((out_channels / 2)), 1), nn.BatchNorm2d(int((out_channels / 2))), nn.ReLU(inplace=True))
    else:
        self.shortcut = nn.Sequential()
        in_channels = int((in_channels / 2))
        self.residual = nn.Sequential(nn.Conv2d(in_channels, in_channels, 1), nn.BatchNorm2d(in_channels), nn.ReLU(inplace=True), nn.Conv2d(in_channels, in_channels, 3, stride=stride, padding=1, groups=in_channels), nn.BatchNorm2d(in_channels), nn.Conv2d(in_channels, in_channels, 1), nn.BatchNorm2d(in_channels), nn.ReLU(inplace=True))
