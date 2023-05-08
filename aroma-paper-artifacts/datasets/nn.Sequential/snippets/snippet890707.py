import torch.nn as nn
import torch.nn.functional as F
import math
from torch.nn import init


def _make_layer(self, block, planes, num_blocks, stride, droprate):
    strides = ([stride] + ([1] * (num_blocks - 1)))
    layers = []
    for stride in strides:
        layers.append(block(self.in_planes, planes, stride, droprate))
        self.in_planes = (planes * block.expansion)
    return nn.Sequential(*layers)
