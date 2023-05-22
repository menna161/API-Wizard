import torch.nn as nn
import math
import torch.utils.model_zoo as model_zoo
import mmd
import torch


def _make_layer(self, block, planes, blocks, stride=1, norm_layer=None):
    if (norm_layer is None):
        norm_layer = nn.BatchNorm2d
    downsample = None
    if ((stride != 1) or (self.inplanes != (planes * block.expansion))):
        downsample = nn.Sequential(conv1x1(self.inplanes, (planes * block.expansion), stride), norm_layer((planes * block.expansion)))
    layers = []
    layers.append(block(self.inplanes, planes, stride, downsample, self.groups, self.base_width, norm_layer))
    self.inplanes = (planes * block.expansion)
    for _ in range(1, blocks):
        layers.append(block(self.inplanes, planes, groups=self.groups, base_width=self.base_width, norm_layer=norm_layer))
    return nn.Sequential(*layers)
