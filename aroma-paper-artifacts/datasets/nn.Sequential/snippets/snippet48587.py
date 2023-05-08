from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import torch
import torch.nn as nn
import torch.utils.model_zoo as model_zoo


def __init__(self, block, layers, heads, head_conv, **kwargs):
    self.inplanes = 64
    self.deconv_with_bias = False
    self.heads = heads
    super(PoseResNet, self).__init__()
    self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
    self.bn1 = nn.BatchNorm2d(64, momentum=BN_MOMENTUM)
    self.relu = nn.ReLU(inplace=True)
    self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
    self.layer1 = self._make_layer(block, 64, layers[0])
    self.layer2 = self._make_layer(block, 128, layers[1], stride=2)
    self.layer3 = self._make_layer(block, 256, layers[2], stride=2)
    self.layer4 = self._make_layer(block, 512, layers[3], stride=2)
    self.deconv_layers = self._make_deconv_layer(3, [256, 256, 256], [4, 4, 4])
    for head in sorted(self.heads):
        num_output = self.heads[head]
        if (head_conv > 0):
            fc = nn.Sequential(nn.Conv2d(256, head_conv, kernel_size=3, padding=1, bias=True), nn.ReLU(inplace=True), nn.Conv2d(head_conv, num_output, kernel_size=1, stride=1, padding=0))
        else:
            fc = nn.Conv2d(in_channels=256, out_channels=num_output, kernel_size=1, stride=1, padding=0)
        self.__setattr__(head, fc)
