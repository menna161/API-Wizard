import os
import sys
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from collections import OrderedDict
from .sadecoder import SADecoder
from sadecoder import SADecoder


def _make_layer(self, block, planes, blocks, stride=1, dilation=1):
    downsample = None
    if ((stride != 1) or (self.inplanes != (planes * block.expansion))):
        downsample = nn.Sequential(nn.Conv2d(self.inplanes, (planes * block.expansion), kernel_size=1, stride=stride, bias=False), nn.BatchNorm2d((planes * block.expansion)))
    layers = []
    layers.append(block(self.inplanes, planes, stride=stride, dilation=dilation, downsample=downsample))
    self.inplanes = (planes * block.expansion)
    for i in range(1, blocks):
        layers.append(block(self.inplanes, planes, stride=1, dilation=dilation))
    return nn.Sequential(*layers)
