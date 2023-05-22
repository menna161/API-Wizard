import torch.nn as nn
import torch.utils.model_zoo as model_zoo
from models_lpf import *


def _make_layer(self, block, planes, blocks, stride=1, groups=1, norm_layer=None, filter_size=1):
    if (norm_layer is None):
        norm_layer = nn.BatchNorm2d
    downsample = None
    if ((stride != 1) or (self.inplanes != (planes * block.expansion))):
        downsample = ([Downsample(filt_size=filter_size, stride=stride, channels=self.inplanes)] if (stride != 1) else [])
        downsample += [conv1x1(self.inplanes, (planes * block.expansion), 1), norm_layer((planes * block.expansion))]
        downsample = nn.Sequential(*downsample)
    layers = []
    layers.append(block(self.inplanes, planes, stride, downsample, groups, norm_layer, filter_size=filter_size))
    self.inplanes = (planes * block.expansion)
    for _ in range(1, blocks):
        layers.append(block(self.inplanes, planes, groups=groups, norm_layer=norm_layer, filter_size=filter_size))
    return nn.Sequential(*layers)
