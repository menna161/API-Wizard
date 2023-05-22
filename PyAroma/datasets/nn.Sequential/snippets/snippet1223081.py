import torch
from torch import nn
from torch.nn import functional as F
from torch.distributions.uniform import Uniform
from networks.layers.non_linear import NonLinear, NonLinearType
from networks.layers.conv_bn import ConvBN


def __init__(self, nc, in_channels, reduce_channels):
    '\n        An implantation of Squeeze Excite block\n\n        :param nc: Input network controller\n        :param in_channels: the number of input channels\n        :param reduce_channels: the number of channels after reduction\n        '
    super(SEBlock, self).__init__()
    self.gap = GlobalAvgPool2d()
    self.conv_reduce = nn.Sequential(ConvBN(nc, in_channels, reduce_channels, 1, disable_bn=True), NonLinear(nc, reduce_channels, NonLinearType.SWISH))
    self.conv_expand = nn.Sequential(ConvBN(nc, reduce_channels, in_channels, 1, disable_bn=True), NonLinear(nc, in_channels, NonLinearType.SIGMOID))
