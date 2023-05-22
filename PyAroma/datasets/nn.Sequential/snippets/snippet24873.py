import torch
import torch.nn as nn
import numpy as np


def _make_layer(self, block, planes, blocks, stride=1, dilate=False):
    norm_layer = self._norm_layer
    downsample = None
    previous_dilation = self.dilation
    output_channel = self.channel_index.pop(0)
    if dilate:
        self.dilation *= stride
        stride = 1
    if ((stride != 1) or (self.inplanes != (planes * block.expansion))):
        downsample = nn.Sequential(conv1x1(self.input_channel, output_channel, stride), norm_layer(output_channel))
    layers = []
    layers.append(block(output_channel, self.channel_index, self.input_channel, stride, downsample, self.groups, previous_dilation, norm_layer))
    self.inplanes = (planes * block.expansion)
    self.input_channel = output_channel
    for _ in range(1, blocks):
        layers.append(block(output_channel, self.channel_index, self.input_channel, groups=self.groups, dilation=self.dilation, norm_layer=norm_layer))
    return nn.Sequential(*layers)
