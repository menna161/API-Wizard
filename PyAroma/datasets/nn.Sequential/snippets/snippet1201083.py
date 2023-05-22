import torch
import torch.nn as nn


def encoder(self, in_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=True, batchnorm=False):
    if batchnorm:
        layer = nn.Sequential(nn.Conv3d(in_channels, out_channels, kernel_size, stride=stride, padding=padding, bias=bias), nn.BatchNorm2d(out_channels), nn.ReLU())
    else:
        layer = nn.Sequential(nn.Conv3d(in_channels, out_channels, kernel_size, stride=stride, padding=padding, bias=bias), nn.ReLU())
    return layer
