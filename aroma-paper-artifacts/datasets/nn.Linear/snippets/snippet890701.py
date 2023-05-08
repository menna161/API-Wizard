import torch.nn as nn
import torch.nn.functional as F
import math
from torch.nn import init


def __init__(self, block, num_blocks, num_classes=10, in_channels=3):
    super(PreActResNet, self).__init__()
    self.in_planes = 64
    last_planes = (512 * block.expansion)
    self.conv1 = conv3x3(in_channels, 64)
    self.stage1 = self._make_layer(block, 64, num_blocks[0], stride=1)
    self.stage2 = self._make_layer(block, 128, num_blocks[1], stride=2)
    self.stage3 = self._make_layer(block, 256, num_blocks[2], stride=2)
    self.stage4 = self._make_layer(block, 512, num_blocks[3], stride=2)
    self.bn_last = nn.BatchNorm2d(last_planes)
    self.last = nn.Linear(last_planes, num_classes)
