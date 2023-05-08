import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parameter import Parameter
from utils.utils import mIoULoss, to_one_hot


def __init__(self, in_channels, out_channels, internal_ratio=4, return_indices=False, dropout_prob=0, bias=False, relu=True):
    super().__init__()
    self.return_indices = return_indices
    if ((internal_ratio <= 1) or (internal_ratio > in_channels)):
        raise RuntimeError('Value out of range. Expected value in the interval [1, {0}], got internal_scale={1}. '.format(in_channels, internal_ratio))
    internal_channels = (in_channels // internal_ratio)
    if relu:
        activation = nn.ReLU
    else:
        activation = nn.PReLU
    self.main_max1 = nn.MaxPool2d(2, stride=2, return_indices=return_indices)
    self.ext_conv1 = nn.Sequential(nn.Conv2d(in_channels, internal_channels, kernel_size=2, stride=2, bias=bias), nn.BatchNorm2d(internal_channels), activation())
    self.ext_conv2 = nn.Sequential(nn.Conv2d(internal_channels, internal_channels, kernel_size=3, stride=1, padding=1, bias=bias), nn.BatchNorm2d(internal_channels), activation())
    self.ext_conv3 = nn.Sequential(nn.Conv2d(internal_channels, out_channels, kernel_size=1, stride=1, bias=bias), nn.BatchNorm2d(out_channels), activation())
    self.ext_regul = nn.Dropout2d(p=dropout_prob)
    self.out_activation = activation()
