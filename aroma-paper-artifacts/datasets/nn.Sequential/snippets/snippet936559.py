import torch.nn as nn
import math
from qtorch import FloatingPoint
from qtorch.quant import Quantizer


def _make_layer(self, block, planes, blocks, quant, stride=1):
    downsample = None
    if ((stride != 1) or (self.inplanes != (planes * block.expansion))):
        downsample = nn.Sequential(nn.Conv2d(self.inplanes, (planes * block.expansion), kernel_size=1, stride=stride, bias=False))
    layers = list()
    layers.append(block(self.inplanes, planes, quant, stride, downsample))
    self.inplanes = (planes * block.expansion)
    for i in range(1, blocks):
        layers.append(block(self.inplanes, planes, quant))
    return nn.Sequential(*layers)
