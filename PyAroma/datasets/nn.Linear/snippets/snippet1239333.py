import os
import sys
import torch
import torch.nn as nn
import math
from lib.nn import SynchronizedBatchNorm2d
from urllib import urlretrieve
from torch.nn import BatchNorm2d as SynchronizedBatchNorm2d
from urllib.request import urlretrieve


def __init__(self, block, layers, groups=32, num_classes=1000):
    self.inplanes = 128
    super(ResNeXt, self).__init__()
    self.conv1 = conv3x3(3, 64, stride=2)
    self.bn1 = SynchronizedBatchNorm2d(64)
    self.relu1 = nn.ReLU(inplace=True)
    self.conv2 = conv3x3(64, 64)
    self.bn2 = SynchronizedBatchNorm2d(64)
    self.relu2 = nn.ReLU(inplace=True)
    self.conv3 = conv3x3(64, 128)
    self.bn3 = SynchronizedBatchNorm2d(128)
    self.relu3 = nn.ReLU(inplace=True)
    self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
    self.layer1 = self._make_layer(block, 128, layers[0], groups=groups)
    self.layer2 = self._make_layer(block, 256, layers[1], stride=2, groups=groups)
    self.layer3 = self._make_layer(block, 512, layers[2], stride=2, groups=groups)
    self.layer4 = self._make_layer(block, 1024, layers[3], stride=2, groups=groups)
    self.avgpool = nn.AvgPool2d(7, stride=1)
    self.fc = nn.Linear((1024 * block.expansion), num_classes)
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            n = (((m.kernel_size[0] * m.kernel_size[1]) * m.out_channels) // m.groups)
            m.weight.data.normal_(0, math.sqrt((2.0 / n)))
        elif isinstance(m, SynchronizedBatchNorm2d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
