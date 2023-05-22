import torch.nn as nn
import torch.nn.functional as F
from .module import ConvModule, xavier_init
import torch


def __init__(self, channels, levels, init=0.5, conv_cfg=None, norm_cfg=None, activation=None, eps=0.0001):
    super(BiFPNModule, self).__init__()
    self.activation = activation
    self.eps = eps
    self.levels = levels
    self.bifpn_convs = nn.ModuleList()
    self.w1 = nn.Parameter(torch.Tensor(2, levels).fill_(init))
    self.relu1 = nn.ReLU()
    self.w2 = nn.Parameter(torch.Tensor(3, (levels - 2)).fill_(init))
    self.relu2 = nn.ReLU()
    for jj in range(2):
        for i in range((self.levels - 1)):
            fpn_conv = nn.Sequential(ConvModule(channels, channels, 3, padding=1, conv_cfg=conv_cfg, norm_cfg=norm_cfg, activation=self.activation, inplace=False))
            self.bifpn_convs.append(fpn_conv)
