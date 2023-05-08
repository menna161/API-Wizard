import torch.nn as nn
from base.base_net import BaseNet
from networks.cbam import CBAM
from torch.nn import init


def _make_layer(self, block, planes, blocks, stride=1, att_type=None):
    downsample = None
    if ((stride != 1) or (self.inplanes != (planes * block.expansion))):
        downsample = nn.Sequential(nn.Conv2d(self.inplanes, (planes * block.expansion), kernel_size=1, stride=stride, bias=False), nn.BatchNorm2d((planes * block.expansion)))
    layers = []
    layers.append(block(self.inplanes, planes, stride, downsample, use_cbam=(att_type == 'CBAM')))
    self.inplanes = (planes * block.expansion)
    for i in range(1, blocks):
        layers.append(block(self.inplanes, planes, use_cbam=(att_type == 'CBAM')))
    return nn.Sequential(*layers)
