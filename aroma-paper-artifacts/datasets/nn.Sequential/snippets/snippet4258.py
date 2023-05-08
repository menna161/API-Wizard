import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parameter import Parameter
from utils.utils import mIoULoss, to_one_hot


def __init__(self, in_channels, out_channels, internal_ratio=4, dropout_prob=0, bias=False, relu=True):
    super().__init__()
    if ((internal_ratio <= 1) or (internal_ratio > in_channels)):
        raise RuntimeError('Value out of range. Expected value in the interval [1, {0}], got internal_scale={1}. '.format(in_channels, internal_ratio))
    internal_channels = (in_channels // internal_ratio)
    if relu:
        activation = nn.ReLU
    else:
        activation = nn.PReLU
    self.main_conv1 = nn.Sequential(nn.Conv2d(in_channels, out_channels, kernel_size=1, bias=bias), nn.BatchNorm2d(out_channels))
    self.main_unpool1 = nn.MaxUnpool2d(kernel_size=2)
    self.ext_conv1 = nn.Sequential(nn.Conv2d(in_channels, internal_channels, kernel_size=1, bias=bias), nn.BatchNorm2d(internal_channels), activation())
    self.ext_tconv1 = nn.ConvTranspose2d(internal_channels, internal_channels, kernel_size=2, stride=2, bias=bias)
    self.ext_tconv1_bnorm = nn.BatchNorm2d(internal_channels)
    self.ext_tconv1_activation = activation()
    self.ext_conv2 = nn.Sequential(nn.Conv2d(internal_channels, out_channels, kernel_size=1, bias=bias), nn.BatchNorm2d(out_channels), activation())
    self.ext_regul = nn.Dropout2d(p=dropout_prob)
    self.out_activation = activation()
