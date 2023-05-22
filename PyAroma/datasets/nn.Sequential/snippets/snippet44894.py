import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import math
from functools import partial


def _make_layer(self, block, planes, blocks, shortcut_type, stride=1):
    downsample = None
    if ((stride != 1) or (self.inplanes != (planes * block.expansion))):
        if (shortcut_type == 'A'):
            downsample = partial(downsample_basic_block, planes=(planes * block.expansion), stride=stride)
        else:
            downsample = nn.Sequential(nn.Conv3d(self.inplanes, (planes * block.expansion), kernel_size=1, stride=stride, bias=False), nn.BatchNorm3d((planes * block.expansion)))
    layers = []
    layers.append(block(self.inplanes, planes, stride, downsample))
    self.inplanes = (planes * block.expansion)
    for i in range(1, blocks):
        layers.append(block(self.inplanes, planes))
    return nn.Sequential(*layers)
