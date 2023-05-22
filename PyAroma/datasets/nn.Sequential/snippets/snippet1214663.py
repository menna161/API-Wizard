from __future__ import print_function, division, absolute_import
import math
from collections import OrderedDict
import torch
import torch.nn as nn


def _make_layer(self, block, planes, blocks, groups, reduction, stride=1, downsample_kernel_size=1, downsample_padding=0):
    downsample = None
    if ((stride != 1) or (self.inplanes != (planes * block.expansion))):
        downsample = nn.Sequential(nn.Conv2d(self.inplanes, (planes * block.expansion), kernel_size=downsample_kernel_size, stride=stride, padding=downsample_padding, bias=False), nn.BatchNorm2d((planes * block.expansion)))
    layers = []
    layers.append(block(self.inplanes, planes, groups, reduction, stride, downsample))
    self.inplanes = (planes * block.expansion)
    for i in range(1, blocks):
        layers.append(block(self.inplanes, planes, groups, reduction))
    return nn.Sequential(*layers)
