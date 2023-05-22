from torch import nn
from models_lpf import *


def __init__(self, inp, oup, stride, expand_ratio, filter_size=1):
    super(InvertedResidual, self).__init__()
    self.stride = stride
    assert (stride in [1, 2])
    hidden_dim = int(round((inp * expand_ratio)))
    self.use_res_connect = ((self.stride == 1) and (inp == oup))
    layers = []
    if (expand_ratio != 1):
        layers.append(ConvBNReLU(inp, hidden_dim, kernel_size=1))
    if (stride == 1):
        layers.extend([ConvBNReLU(hidden_dim, hidden_dim, stride=stride, groups=hidden_dim), nn.Conv2d(hidden_dim, oup, 1, 1, 0, bias=False), nn.BatchNorm2d(oup)])
    else:
        layers.extend([ConvBNReLU(hidden_dim, hidden_dim, stride=1, groups=hidden_dim), Downsample(filt_size=filter_size, stride=stride, channels=hidden_dim), nn.Conv2d(hidden_dim, oup, 1, 1, 0, bias=False), nn.BatchNorm2d(oup)])
    self.conv = nn.Sequential(*layers)
