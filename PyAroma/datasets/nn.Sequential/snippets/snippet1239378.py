import os
import sys
import torch
import torch.nn as nn
import math
from lib.nn import SynchronizedBatchNorm2d
from urllib import urlretrieve
from torch.nn import BatchNorm2d as SynchronizedBatchNorm2d
from urllib.request import urlretrieve


def _make_layer(self, block, planes, blocks, stride=1):
    downsample = None
    if ((stride != 1) or (self.inplanes != (planes * block.expansion))):
        downsample = nn.Sequential(nn.Conv2d(self.inplanes, (planes * block.expansion), kernel_size=1, stride=stride, bias=False), SynchronizedBatchNorm2d((planes * block.expansion)))
    layers = []
    layers.append(block(self.inplanes, planes, stride, downsample))
    self.inplanes = (planes * block.expansion)
    for i in range(1, blocks):
        layers.append(block(self.inplanes, planes))
    return nn.Sequential(*layers)
