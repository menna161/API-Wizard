from __future__ import absolute_import
import torch.nn as nn
import math


def __init__(self, depth, in_channels=3, num_classes=10, block_name='BasicBlock'):
    super(ResNet, self).__init__()
    if (block_name.lower() == 'basicblock'):
        assert (((depth - 2) % 6) == 0), 'When use basicblock, depth should be 6n+2, e.g. 20, 32, 44, 56, 110, 1202'
        n = ((depth - 2) // 6)
        block = BasicBlock
    elif (block_name.lower() == 'bottleneck'):
        assert (((depth - 2) % 9) == 0), 'When use bottleneck, depth should be 9n+2, e.g. 20, 29, 47, 56, 110, 1199'
        n = ((depth - 2) // 9)
        block = Bottleneck
    else:
        raise ValueError('block_name shoule be Basicblock or Bottleneck')
    self.inplanes = 16
    self.conv1 = nn.Conv2d(in_channels, 16, kernel_size=3, padding=1, bias=False)
    self.bn1 = nn.BatchNorm2d(16)
    self.relu = nn.ReLU(inplace=True)
    self.layer1 = self._make_layer(block, 16, n)
    self.layer2 = self._make_layer(block, 32, n, stride=2)
    self.layer3 = self._make_layer(block, 64, n, stride=2)
    self.avgpool = nn.AvgPool2d(8)
    self.fc = nn.Linear((64 * block.expansion), num_classes)
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            n = ((m.kernel_size[0] * m.kernel_size[1]) * m.out_channels)
            m.weight.data.normal_(0, math.sqrt((2.0 / n)))
        elif isinstance(m, nn.BatchNorm2d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
