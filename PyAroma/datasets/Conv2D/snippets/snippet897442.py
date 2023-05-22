import functools
import torch
from torch import nn
import torch.nn.functional as F
from torch.nn.modules.conv import _ConvNd
from torch.nn.modules.utils import _pair
from torch.nn.parameter import Parameter


def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, bias=True, padding_mode='zeros', num_experts=3, dropout_rate=0.2):
    kernel_size = _pair(kernel_size)
    stride = _pair(stride)
    padding = _pair(padding)
    dilation = _pair(dilation)
    super(CondConv2D, self).__init__(in_channels, out_channels, kernel_size, stride, padding, dilation, False, _pair(0), groups, bias, padding_mode)
    self._avg_pooling = functools.partial(F.adaptive_avg_pool2d, output_size=(1, 1))
    self._routing_fn = _routing(in_channels, num_experts, dropout_rate)
    self.weight = Parameter(torch.Tensor(num_experts, out_channels, (in_channels // groups), *kernel_size))
    self.reset_parameters()
