import torch
import torch.nn as nn
from torchvision.models.utils import load_state_dict_from_url
from networks.layers.non_linear import NonLinear
from networks.layers.conv_bn import ConvBN


def _make_layer(self, block, planes, blocks, stride=1, dilate=False):
    downsample = None
    previous_dilation = self.dilation
    if dilate:
        self.dilation *= stride
        stride = 1
    if ((stride != 1) or (self.inplanes != (planes * block.expansion))):
        downsample = conv1x1_bn(self.nc, self.inplanes, (planes * block.expansion), stride)
    layers = []
    layers.append(block(self.nc, self.inplanes, planes, stride, downsample, self.groups, self.base_width, previous_dilation))
    self.inplanes = (planes * block.expansion)
    for _ in range(1, blocks):
        layers.append(block(self.nc, self.inplanes, planes, groups=self.groups, base_width=self.base_width, dilation=self.dilation))
    return nn.Sequential(*layers)
