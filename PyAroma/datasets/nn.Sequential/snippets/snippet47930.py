from collections import OrderedDict
import torch
import torch.nn as nn


def __init__(self, l, fan_in, fan_out, kernel_size=3, padding=1, stride=1, batch_norm=1e-05, is_transposed=False):
    super(SingleConvLayer, self).__init__()
    if is_transposed:
        self.layer = nn.Sequential(OrderedDict([(('transposed_conv' + str(l)), nn.ConvTranspose2d(fan_in, fan_out, kernel_size=kernel_size, padding=padding, stride=stride, bias=False))]))
    else:
        self.layer = nn.Sequential(OrderedDict([(('conv' + str(l)), nn.Conv2d(fan_in, fan_out, kernel_size=kernel_size, padding=padding, stride=stride, bias=False))]))
    if (batch_norm > 0.0):
        self.layer.add_module(('bn' + str(l)), nn.BatchNorm2d(fan_out, eps=batch_norm))
    self.layer.add_module(('act' + str(l)), nn.ReLU())
