import torch.nn as nn
from octconv import *


def _make_layer(self, block, planes, blocks, stride=1, alpha_in=0.5, alpha_out=0.5, norm_layer=None, output=False):
    if (norm_layer is None):
        norm_layer = nn.BatchNorm2d
    downsample = None
    if ((stride != 1) or (self.inplanes != (planes * block.expansion))):
        downsample = nn.Sequential(Conv_BN(self.inplanes, (planes * block.expansion), kernel_size=1, stride=stride, alpha_in=alpha_in, alpha_out=alpha_out))
    layers = []
    layers.append(block(self.inplanes, planes, stride, downsample, self.groups, self.base_width, alpha_in, alpha_out, norm_layer, output))
    self.inplanes = (planes * block.expansion)
    for _ in range(1, blocks):
        layers.append(block(self.inplanes, planes, groups=self.groups, base_width=self.base_width, norm_layer=norm_layer, alpha_in=(0 if output else 0.5), alpha_out=(0 if output else 0.5), output=output))
    return nn.Sequential(*layers)
