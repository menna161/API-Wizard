from __future__ import absolute_import
import torch
from torch import nn
from torch.nn import functional as F
import torchvision


def __init__(self, in_channel=1, out_channel=16, kernels=[11, 7, 5, 3, 3], mid_channel=16):
    super(SparseConvNet, self).__init__()
    channel = in_channel
    convs = []
    for i in range(len(kernels)):
        if (i % 2):
            stride = 2
        else:
            stride = 1
        assert ((kernels[i] % 2) == 1)
        convs += [SparseConvBlock(channel, mid_channel, kernels[i], stride=stride, padding=((kernels[i] - 1) // 2))]
        channel = mid_channel
    self.sparse_convs = nn.Sequential(*convs)
    self.mask_conv = nn.Conv2d((mid_channel + 1), out_channel, 1)
