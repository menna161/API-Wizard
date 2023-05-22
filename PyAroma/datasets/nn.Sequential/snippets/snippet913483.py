import torch
import torch.nn as nn
import os
from util.download_from_url import download_from_url
from torch.hub import _get_torch_home


def _make_layer(self, block, planes, blocks, stride=1, norm_layer=None):
    if (norm_layer is None):
        norm_layer = nn.BatchNorm2d
    downsample = None
    if ((stride != 1) or (self.inplanes != (planes * block.expansion))):
        downsample = nn.Sequential(conv1x1(self.inplanes, (planes * block.expansion), stride), norm_layer((planes * block.expansion)))
    layers = []
    layers.append(block(self.inplanes, planes, stride, downsample, norm_layer))
    self.inplanes = (planes * block.expansion)
    for _ in range(1, blocks):
        layers.append(block(self.inplanes, planes, norm_layer=norm_layer))
    return nn.Sequential(*layers)
