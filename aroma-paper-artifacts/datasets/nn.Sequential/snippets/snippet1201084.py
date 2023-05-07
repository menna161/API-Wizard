import torch
import torch.nn as nn


def decoder(self, in_channels, out_channels, kernel_size, stride=1, padding=0, output_padding=0, bias=True):
    layer = nn.Sequential(nn.ConvTranspose3d(in_channels, out_channels, kernel_size, stride=stride, padding=padding, output_padding=output_padding, bias=bias), nn.ReLU())
    return layer
