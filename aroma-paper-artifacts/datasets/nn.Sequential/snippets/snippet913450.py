import torch
import torch.nn as nn
import os
from util.download_from_url import download_from_url
from torch.hub import _get_torch_home


def _make_layer(self, block, planes, blocks, stride=1, norm_layer=None, pyconv_kernels=[3], pyconv_groups=[1]):
    if (norm_layer is None):
        norm_layer = nn.BatchNorm2d
    downsample = None
    if ((stride != 1) and (self.inplanes != (planes * block.expansion))):
        downsample = nn.Sequential(nn.MaxPool2d(kernel_size=3, stride=stride, padding=1), conv1x1(self.inplanes, (planes * block.expansion)), norm_layer((planes * block.expansion)))
    elif (self.inplanes != (planes * block.expansion)):
        downsample = nn.Sequential(conv1x1(self.inplanes, (planes * block.expansion)), norm_layer((planes * block.expansion)))
    elif (stride != 1):
        downsample = nn.MaxPool2d(kernel_size=3, stride=stride, padding=1)
    layers = []
    layers.append(block(self.inplanes, planes, stride=stride, downsample=downsample, norm_layer=norm_layer, pyconv_kernels=pyconv_kernels, pyconv_groups=pyconv_groups))
    self.inplanes = (planes * block.expansion)
    for _ in range(1, blocks):
        layers.append(block(self.inplanes, planes, norm_layer=norm_layer, pyconv_kernels=pyconv_kernels, pyconv_groups=pyconv_groups))
    return nn.Sequential(*layers)
