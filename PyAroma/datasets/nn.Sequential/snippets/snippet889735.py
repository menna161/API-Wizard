import torch.nn as nn
import math


def __init__(self, inp, hidden_dim, oup, kernel_size, stride, use_se, use_hs):
    super(InvertedResidual, self).__init__()
    assert (stride in [1, 2])
    self.identity = ((stride == 1) and (inp == oup))
    if (inp == hidden_dim):
        self.conv = nn.Sequential(nn.Conv2d(hidden_dim, hidden_dim, kernel_size, stride, ((kernel_size - 1) // 2), groups=hidden_dim, bias=False), nn.BatchNorm2d(hidden_dim), (h_swish() if use_hs else nn.ReLU(inplace=True)), (SELayer(hidden_dim) if use_se else nn.Identity()), nn.Conv2d(hidden_dim, oup, 1, 1, 0, bias=False), nn.BatchNorm2d(oup))
    else:
        self.conv = nn.Sequential(nn.Conv2d(inp, hidden_dim, 1, 1, 0, bias=False), nn.BatchNorm2d(hidden_dim), (h_swish() if use_hs else nn.ReLU(inplace=True)), nn.Conv2d(hidden_dim, hidden_dim, kernel_size, stride, ((kernel_size - 1) // 2), groups=hidden_dim, bias=False), nn.BatchNorm2d(hidden_dim), (SELayer(hidden_dim) if use_se else nn.Identity()), (h_swish() if use_hs else nn.ReLU(inplace=True)), nn.Conv2d(hidden_dim, oup, 1, 1, 0, bias=False), nn.BatchNorm2d(oup))
