from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import math
from os.path import join
import torch
from torch import nn
import torch.utils.model_zoo as model_zoo
import numpy as np


def __init__(self, node_kernel, out_dim, channels, up_factors):
    super(IDAUp, self).__init__()
    self.channels = channels
    self.out_dim = out_dim
    for (i, c) in enumerate(channels):
        if (c == out_dim):
            proj = Identity()
        else:
            proj = nn.Sequential(nn.Conv2d(c, out_dim, kernel_size=1, stride=1, bias=False), BatchNorm(out_dim), nn.ReLU(inplace=True))
        f = int(up_factors[i])
        if (f == 1):
            up = Identity()
        else:
            up = nn.ConvTranspose2d(out_dim, out_dim, (f * 2), stride=f, padding=(f // 2), output_padding=0, groups=out_dim, bias=False)
            fill_up_weights(up)
        setattr(self, ('proj_' + str(i)), proj)
        setattr(self, ('up_' + str(i)), up)
    for i in range(1, len(channels)):
        node = nn.Sequential(nn.Conv2d((out_dim * 2), out_dim, kernel_size=node_kernel, stride=1, padding=(node_kernel // 2), bias=False), BatchNorm(out_dim), nn.ReLU(inplace=True))
        setattr(self, ('node_' + str(i)), node)
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            n = ((m.kernel_size[0] * m.kernel_size[1]) * m.out_channels)
            m.weight.data.normal_(0, math.sqrt((2.0 / n)))
        elif isinstance(m, BatchNorm):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
