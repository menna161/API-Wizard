import torch
import torch.nn as nn
import torch.nn.functional as F


def _make_layer(self, block, planes, blocks, stride=1, dilation=1):
    downsample = None
    if ((stride != 1) or (self.inplanes != (planes * block.expansion)) or (dilation == 2) or (dilation == 4)):
        downsample = nn.Sequential(nn.Conv2d(self.inplanes, (planes * block.expansion), kernel_size=1, stride=stride, bias=False), nn.BatchNorm2d((planes * block.expansion), affine=affine_par))
    layers = []
    layers.append(block(self.inplanes, planes, stride, dilation=dilation, downsample=downsample))
    self.inplanes = (planes * block.expansion)
    for i in range(1, blocks):
        layers.append(block(self.inplanes, planes, dilation=dilation))
    return nn.Sequential(*layers)
