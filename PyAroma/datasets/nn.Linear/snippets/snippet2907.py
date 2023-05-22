import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


def __init__(self, input_nc=3, num_classes=10, **kwargs):
    super(ResNet, self).__init__()
    self.in_planes = 64
    block = BasicBlock
    num_blocks = [2, 2, 2, 2, 2]
    self.conv1 = nn.Conv2d(input_nc, 64, kernel_size=3, stride=1, padding=1, bias=False)
    self.bn1 = nn.BatchNorm2d(64)
    self.layer1 = self._make_layer(block, 64, num_blocks[0], stride=1)
    self.layer2 = self._make_layer(block, 128, num_blocks[1], stride=2)
    self.layer3 = self._make_layer(block, 256, num_blocks[2], stride=2)
    self.layer4 = self._make_layer(block, 512, num_blocks[3], stride=2)
    self.avgpool = nn.AdaptiveAvgPool2d(output_size=(1, 1))
    self.linear1 = nn.Linear(512, 1024)
    self.linear2 = nn.Linear(1024, num_classes)
