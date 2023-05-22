import torch
from torch import nn
from torch.nn import functional as F
import pdb


def __init__(self, in_channels, reduction=2, mode='embedded_gaussian'):
    super(ModulatedAttLayer, self).__init__()
    self.in_channels = in_channels
    self.reduction = reduction
    self.inter_channels = (in_channels // reduction)
    self.mode = mode
    assert (mode in ['embedded_gaussian'])
    self.g = nn.Conv2d(self.in_channels, self.inter_channels, kernel_size=1)
    self.theta = nn.Conv2d(self.in_channels, self.inter_channels, kernel_size=1)
    self.phi = nn.Conv2d(self.in_channels, self.inter_channels, kernel_size=1)
    self.conv_mask = nn.Conv2d(self.inter_channels, self.in_channels, kernel_size=1, bias=False)
    self.relu = nn.ReLU(inplace=True)
    self.avgpool = nn.AvgPool2d(7, stride=1)
    self.fc_spatial = nn.Linear(((7 * 7) * self.in_channels), (7 * 7))
    self.init_weights()
