import torch
import torch.nn as nn
import math
from torch.nn.modules.batchnorm import _BatchNorm


def _make_layer(self, block, planes, blocks, kernel, stride=1):
    downsample = None
    if ((stride != 1) or (self.inplanes != (planes * block.expansion))):
        downsample = nn.Sequential(nn.Conv3d(self.inplanes, (planes * block.expansion), kernel_size=1, stride=stride, bias=False), nn.BatchNorm3d((planes * block.expansion)))
    layers = []
    layers.append(block(self.inplanes, planes, stride, kernel[0], downsample, self.groups, self.base_width))
    self.inplanes = (planes * block.expansion)
    for i in range(1, blocks):
        layers.append(block(self.inplanes, planes, kernel=kernel[i], groups=self.groups, base_width=self.base_width))
    return nn.Sequential(*layers)
