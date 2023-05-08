import torch
from torch import nn
import torch.nn.functional as F


def __init__(self, in_planes, out_planes, input_sz, bias=True, batch_norm=True, relu=True):
    super().__init__()
    self.linear = nn.Linear(((in_planes * input_sz) * input_sz), out_planes, bias=bias)
    self.bn = (nn.BatchNorm2d(out_planes) if batch_norm else None)
    self.relu = (nn.ReLU(inplace=True) if relu else None)
