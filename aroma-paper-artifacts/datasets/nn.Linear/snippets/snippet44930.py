import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import math
from functools import partial


def __init__(self, block, layers, sample_size, sample_duration, k=1, shortcut_type='B', num_classes=400):
    self.inplanes = 64
    super(WideResNet, self).__init__()
    self.conv1 = nn.Conv3d(3, 64, kernel_size=7, stride=(1, 2, 2), padding=(3, 3, 3), bias=False)
    self.bn1 = nn.BatchNorm3d(64)
    self.relu = nn.ReLU(inplace=True)
    self.maxpool = nn.MaxPool3d(kernel_size=(3, 3, 3), stride=2, padding=1)
    self.layer1 = self._make_layer(block, (64 * k), layers[0], shortcut_type)
    self.layer2 = self._make_layer(block, (128 * k), layers[1], shortcut_type, stride=2)
    self.layer3 = self._make_layer(block, (256 * k), layers[2], shortcut_type, stride=2)
    self.layer4 = self._make_layer(block, (512 * k), layers[3], shortcut_type, stride=2)
    last_duration = int(math.ceil((sample_duration / 16)))
    last_size = int(math.ceil((sample_size / 32)))
    self.avgpool = nn.AvgPool3d((last_duration, last_size, last_size), stride=1)
    self.fc = nn.Linear(((512 * k) * block.expansion), num_classes)
    for m in self.modules():
        if isinstance(m, nn.Conv3d):
            m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
        elif isinstance(m, nn.BatchNorm3d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()