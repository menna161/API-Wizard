import numpy as np
import math
import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, depth, num_classes, widen_factor=1, dropRate=0.0):
    super(WideResNet, self).__init__()
    nChannels = [16, (16 * widen_factor), (32 * widen_factor), (64 * widen_factor)]
    assert (((depth - 4) % 6) == 0), 'depth should be 6n+4'
    n = ((depth - 4) // 6)
    block = BasicBlock
    self.conv1 = nn.Conv2d(3, nChannels[0], kernel_size=3, stride=1, padding=1, bias=False)
    self.block1 = NetworkBlock(n, nChannels[0], nChannels[1], block, 1, dropRate)
    self.block2 = NetworkBlock(n, nChannels[1], nChannels[2], block, 2, dropRate)
    self.block3 = NetworkBlock(n, nChannels[2], nChannels[3], block, 2, dropRate)
    self.bn1 = nn.BatchNorm2d(nChannels[3])
    self.relu = nn.ReLU(inplace=True)
    self.fc = nn.Linear(nChannels[3], num_classes)
    self.nChannels = nChannels[3]
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            n = ((m.kernel_size[0] * m.kernel_size[1]) * m.out_channels)
            m.weight.data.normal_(0, math.sqrt((2.0 / n)))
        elif isinstance(m, nn.BatchNorm2d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
        elif isinstance(m, nn.Linear):
            m.bias.data.zero_()
