import torch.nn as nn
import torch.nn.functional as F
import math
from torch.nn import init


def __init__(self, block, num_blocks, filters, num_classes=10, droprate=0):
    super(PreActResNet_cifar, self).__init__()
    self.in_planes = 16
    last_planes = (filters[2] * block.expansion)
    self.conv1 = conv3x3(3, self.in_planes)
    self.stage1 = self._make_layer(block, filters[0], num_blocks[0], stride=1, droprate=droprate)
    self.stage2 = self._make_layer(block, filters[1], num_blocks[1], stride=2, droprate=droprate)
    self.stage3 = self._make_layer(block, filters[2], num_blocks[2], stride=2, droprate=droprate)
    self.bn_last = nn.BatchNorm2d(last_planes)
    self.last = nn.Linear(last_planes, num_classes)
    '\n        for m in self.modules():\n            if isinstance(m, nn.Conv2d):\n                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels\n                m.weight.data.normal_(0, math.sqrt(2. / n))\n                # m.bias.data.zero_()\n            elif isinstance(m, nn.BatchNorm2d):\n                m.weight.data.fill_(1)\n                m.bias.data.zero_()\n            elif isinstance(m, nn.Linear):\n                init.kaiming_normal(m.weight)\n                m.bias.data.zero_()\n        '
