import sys
from collections import OrderedDict
from functools import partial
import torch.nn as nn
import functools


def _make_layer(self, block, planes, blocks, stride=1, dilation=1, multi_grid=1, bn_momentum=0.0003, BatchNorm2d=nn.BatchNorm2d):
    downsample = None
    if ((stride != 1) or (self.inplanes != (planes * block.expansion))):
        downsample = nn.Sequential(nn.Conv2d(self.inplanes, (planes * block.expansion), kernel_size=1, stride=stride, bias=False), BatchNorm2d((planes * block.expansion), affine=True, momentum=bn_momentum))
    layers = []
    generate_multi_grid = (lambda index, grids: (grids[(index % len(grids))] if isinstance(grids, tuple) else 1))
    layers.append(block(self.inplanes, planes, stride, dilation=dilation, downsample=downsample, multi_grid=generate_multi_grid(0, multi_grid), bn_momentum=bn_momentum, BatchNorm2d=BatchNorm2d))
    self.inplanes = (planes * block.expansion)
    for i in range(1, blocks):
        layers.append(block(self.inplanes, planes, dilation=dilation, multi_grid=generate_multi_grid(i, multi_grid), bn_momentum=bn_momentum, BatchNorm2d=BatchNorm2d))
    return nn.Sequential(*layers)
