import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parameter import Parameter
from utils.utils import mIoULoss, to_one_hot


def __init__(self, channels, internal_ratio=4, kernel_size=3, padding=0, dilation=1, asymmetric=False, dropout_prob=0, bias=False, relu=True):
    super().__init__()
    if ((internal_ratio <= 1) or (internal_ratio > channels)):
        raise RuntimeError('Value out of range. Expected value in the interval [1, {0}], got internal_scale={1}.'.format(channels, internal_ratio))
    internal_channels = (channels // internal_ratio)
    if relu:
        activation = nn.ReLU
    else:
        activation = nn.PReLU
    self.ext_conv1 = nn.Sequential(nn.Conv2d(channels, internal_channels, kernel_size=1, stride=1, bias=bias), nn.BatchNorm2d(internal_channels), activation())
    if asymmetric:
        self.ext_conv2 = nn.Sequential(nn.Conv2d(internal_channels, internal_channels, kernel_size=(kernel_size, 1), stride=1, padding=(padding, 0), dilation=dilation, bias=bias), nn.BatchNorm2d(internal_channels), activation(), nn.Conv2d(internal_channels, internal_channels, kernel_size=(1, kernel_size), stride=1, padding=(0, padding), dilation=dilation, bias=bias), nn.BatchNorm2d(internal_channels), activation())
    else:
        self.ext_conv2 = nn.Sequential(nn.Conv2d(internal_channels, internal_channels, kernel_size=kernel_size, stride=1, padding=padding, dilation=dilation, bias=bias), nn.BatchNorm2d(internal_channels), activation())
    self.ext_conv3 = nn.Sequential(nn.Conv2d(internal_channels, channels, kernel_size=1, stride=1, bias=bias), nn.BatchNorm2d(channels), activation())
    self.ext_regul = nn.Dropout2d(p=dropout_prob)
    self.out_activation = activation()
