import torch
import torch.nn.functional as F
import torch.nn as nn
import math
from networks.deeplab.sync_batchnorm.batchnorm import SynchronizedBatchNorm2d
import torch.utils.model_zoo as model_zoo


def __init__(self, inp, oup, stride, dilation, expand_ratio, BatchNorm):
    super(InvertedResidual, self).__init__()
    self.stride = stride
    assert (stride in [1, 2])
    hidden_dim = round((inp * expand_ratio))
    self.use_res_connect = ((self.stride == 1) and (inp == oup))
    self.kernel_size = 3
    self.dilation = dilation
    if (expand_ratio == 1):
        self.conv = nn.Sequential(nn.Conv2d(hidden_dim, hidden_dim, 3, stride, 0, dilation, groups=hidden_dim, bias=False), BatchNorm(hidden_dim), nn.ReLU6(inplace=True), nn.Conv2d(hidden_dim, oup, 1, 1, 0, 1, 1, bias=False), BatchNorm(oup))
    else:
        self.conv = nn.Sequential(nn.Conv2d(inp, hidden_dim, 1, 1, 0, 1, bias=False), BatchNorm(hidden_dim), nn.ReLU6(inplace=True), nn.Conv2d(hidden_dim, hidden_dim, 3, stride, 0, dilation, groups=hidden_dim, bias=False), BatchNorm(hidden_dim), nn.ReLU6(inplace=True), nn.Conv2d(hidden_dim, oup, 1, 1, 0, 1, bias=False), BatchNorm(oup))
