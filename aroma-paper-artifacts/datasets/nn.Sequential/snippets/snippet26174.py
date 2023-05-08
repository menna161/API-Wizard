import math
import torch
import torch.nn as nn


def _make_layer_fast(self, block, planes, blocks, stride=1, head_conv=1):
    downsample = None
    if ((stride != 1) or (self.fast_inplanes != (planes * block.expansion))):
        downsample = nn.Sequential(nn.Conv3d(self.fast_inplanes, (planes * block.expansion), kernel_size=1, stride=(1, stride, stride), bias=False))
    layers = []
    layers.append(block(self.fast_inplanes, planes, stride, downsample, head_conv=head_conv))
    self.fast_inplanes = (planes * block.expansion)
    for i in range(1, blocks):
        layers.append(block(self.fast_inplanes, planes, head_conv=head_conv))
    return nn.Sequential(*layers)
