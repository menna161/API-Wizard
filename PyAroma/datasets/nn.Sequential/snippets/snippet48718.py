import torch
import torch.nn as nn


def __init__(self, k, inp_dim, out_dim, stride=1, with_bn=True):
    super(convolution, self).__init__()
    pad = ((k - 1) // 2)
    self.conv = nn.Conv2d(inp_dim, out_dim, (k, k), padding=(pad, pad), stride=(stride, stride), bias=(not with_bn))
    self.bn = (nn.BatchNorm2d(out_dim) if with_bn else nn.Sequential())
    self.relu = nn.ReLU(inplace=True)
