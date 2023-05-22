import torch
import torch.nn as nn
import torch.utils.model_zoo as model_zoo


def _make_layer(self, block, planes, blocks, stride=1, dilation=1, bn_momentum=0.1, norm_layer=nn.BatchNorm2d):
    downsample = None
    if ((stride != 1) or (self.inplanes != (planes * block.expansion))):
        downsample = nn.Sequential(nn.Conv2d(self.inplanes, (planes * block.expansion), kernel_size=1, stride=stride, bias=False), norm_layer((planes * block.expansion)))
    layers = []
    layers.append(block(self.inplanes, planes, stride, dilation, downsample, bn_momentum=bn_momentum, norm_layer=norm_layer))
    self.inplanes = (planes * block.expansion)
    for i in range(1, blocks):
        layers.append(block(self.inplanes, planes, dilation=dilation, bn_momentum=bn_momentum, norm_layer=norm_layer))
    return nn.Sequential(*layers)
