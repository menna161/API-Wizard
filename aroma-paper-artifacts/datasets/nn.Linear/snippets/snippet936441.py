import math
import torch
import torch.nn as nn


def __init__(self, depth, width, num_classes=10, dropout=0.3):
    super(WideResNet, self).__init__()
    layer = ((depth - 4) // 6)
    self.inplanes = 16
    self.conv = conv3x3(3, 16)
    self.layer1 = self._make_layer((16 * width), layer, dropout)
    self.layer2 = self._make_layer((32 * width), layer, dropout, stride=2)
    self.layer3 = self._make_layer((64 * width), layer, dropout, stride=2)
    self.bn = nn.BatchNorm2d((64 * width))
    self.relu = nn.ReLU(inplace=True)
    self.avgpool = nn.AdaptiveAvgPool2d(1)
    self.fc = nn.Linear((64 * width), num_classes)
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            m.weight.data = nn.init.kaiming_normal_(m.weight.data, mode='fan_out', nonlinearity='relu')
