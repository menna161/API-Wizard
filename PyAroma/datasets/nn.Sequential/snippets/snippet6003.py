import torch
from torch import nn
import torch.nn.functional as F


def conv_block(in_planes, out_planes, kernel_size=3, stride=1, padding=1, dilation=1, bias=True, batch_norm=True, relu=True):
    layers = [nn.Conv2d(in_planes, out_planes, kernel_size=kernel_size, stride=stride, padding=padding, dilation=dilation, bias=bias)]
    if batch_norm:
        layers.append(nn.BatchNorm2d(out_planes))
    if relu:
        layers.append(nn.ReLU(inplace=True))
    return nn.Sequential(*layers)
