import torch.nn as nn
import torch.nn.init as init
import torch.nn.functional as F
import numpy as np


def __init__(self, depth, widen_factor, dropout_rate, num_classes):
    super(WideResNet, self).__init__()
    self.in_planes = 16
    assert (((depth - 4) % 6) == 0), 'Wide-resnet depth should be 6n+4'
    n = int(((depth - 4) / 6))
    k = widen_factor
    nStages = [16, (16 * k), (32 * k), (64 * k)]
    self.conv1 = conv3x3(3, nStages[0])
    self.layer1 = self._wide_layer(WideBasic, nStages[1], n, dropout_rate, stride=1)
    self.layer2 = self._wide_layer(WideBasic, nStages[2], n, dropout_rate, stride=2)
    self.layer3 = self._wide_layer(WideBasic, nStages[3], n, dropout_rate, stride=2)
    self.bn1 = nn.BatchNorm2d(nStages[3], momentum=0.9)
    self.linear = nn.Linear(nStages[3], num_classes)
