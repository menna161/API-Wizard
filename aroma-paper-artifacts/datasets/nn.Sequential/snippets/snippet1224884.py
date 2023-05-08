import functools
import torch.nn as nn
from utils.pyt_utils import load_model


def _make_layer(self, block, norm_layer, planes, blocks, inplace=True, stride=1, bn_eps=1e-05, bn_momentum=0.1):
    downsample = None
    if ((stride != 1) or (self.inplanes != (planes * block.expansion))):
        downsample = nn.Sequential(nn.Conv2d(self.inplanes, (planes * block.expansion), kernel_size=1, stride=stride, bias=False), norm_layer((planes * block.expansion), eps=bn_eps, momentum=bn_momentum))
    layers = []
    layers.append(block(self.inplanes, planes, stride, norm_layer, bn_eps, bn_momentum, downsample, inplace))
    self.inplanes = (planes * block.expansion)
    for i in range(1, blocks):
        layers.append(block(self.inplanes, planes, norm_layer=norm_layer, bn_eps=bn_eps, bn_momentum=bn_momentum, inplace=inplace))
    return nn.Sequential(*layers)
