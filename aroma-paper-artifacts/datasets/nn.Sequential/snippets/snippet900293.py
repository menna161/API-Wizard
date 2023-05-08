import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, in_channels, n_filters, k_size, stride, padding, bias=True):
    super(deconv2DBatchNormRelu, self).__init__()
    self.dcbr_unit = nn.Sequential(nn.ConvTranspose2d(int(in_channels), int(n_filters), kernel_size=k_size, padding=padding, stride=stride, bias=bias), nn.BatchNorm2d(int(n_filters)), nn.ReLU(inplace=True))
