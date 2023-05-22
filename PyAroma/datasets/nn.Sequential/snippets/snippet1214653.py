import torch
import torch.nn as nn
import math
import torch.utils.model_zoo as model_zoo


def _make_layer(self, block, planes, blocks, stride=1):
    downsample = None
    if ((stride != 1) or (self.inplanes != (planes * block.expansion))):
        downsample = nn.Sequential(nn.Conv2d(self.inplanes, (planes * block.expansion), kernel_size=1, stride=stride, bias=False), nn.BatchNorm2d((planes * block.expansion)))
    layers = []
    ibn = True
    if (planes == 512):
        ibn = False
    layers.append(block(self.inplanes, planes, ibn, stride, downsample))
    self.inplanes = (planes * block.expansion)
    for i in range(1, blocks):
        layers.append(block(self.inplanes, planes, ibn))
    return nn.Sequential(*layers)
