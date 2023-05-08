import torch.nn as nn
import math
import torch
import numpy as np
import torch.nn.functional as F


def _make_layer(self, block, planes, blocks, stride=1, dilation__=1):
    downsample = None
    if ((stride != 1) or (self.inplanes != (planes * block.expansion)) or (dilation__ == 2) or (dilation__ == 4)):
        downsample = nn.Sequential(nn.Conv2d(self.inplanes, (planes * block.expansion), kernel_size=1, stride=stride, bias=False), nn.BatchNorm2d((planes * block.expansion), affine=affine_par))
    for i in downsample._modules['1'].parameters():
        i.requires_grad = False
    layers = []
    layers.append(block(self.inplanes, planes, stride, dilation_=dilation__, downsample=downsample))
    self.inplanes = (planes * block.expansion)
    for i in range(1, blocks):
        layers.append(block(self.inplanes, planes, dilation_=dilation__))
    return nn.Sequential(*layers)
