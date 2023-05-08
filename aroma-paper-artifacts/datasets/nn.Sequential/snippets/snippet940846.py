import torch.nn as nn
import torch.utils.model_zoo as model_zoo
import sys
import Utils


def _make_layer(self, block, planes, blocks, padding, stride=1):
    downsample = None
    if ((stride != 1) or (self.inplanes != (planes * block.expansion))):
        downsample = nn.Sequential(conv1x1(self.inplanes, (planes * block.expansion), stride), nn.BatchNorm2d((planes * block.expansion)))
    layers = []
    layers.append(block(self.inplanes, planes, stride, downsample, padding=padding))
    self.inplanes = (planes * block.expansion)
    for _ in range(1, blocks):
        layers.append(block(self.inplanes, planes, padding=padding))
    return nn.Sequential(*layers)
