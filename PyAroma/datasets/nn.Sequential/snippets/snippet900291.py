import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, in_channels, n_filters, k_size, stride, padding, bias=True, dilation=1):
    super(conv2DBatchNormRelu, self).__init__()
    if (dilation > 1):
        conv_mod = nn.Conv2d(int(in_channels), int(n_filters), kernel_size=k_size, padding=padding, stride=stride, bias=bias, dilation=dilation)
    else:
        conv_mod = nn.Conv2d(int(in_channels), int(n_filters), kernel_size=k_size, padding=padding, stride=stride, bias=bias, dilation=1)
    self.cbr_unit = nn.Sequential(conv_mod, nn.BatchNorm2d(int(n_filters)), nn.ReLU(inplace=True))
