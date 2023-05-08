import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, block, num_blocks, num_classes=10, feat_scale=1, wd=1):
    super(ResNet, self).__init__()
    widths = [64, 128, 256, 512]
    widths = [int((w * wd)) for w in widths]
    self.in_planes = widths[0]
    self.conv1 = nn.Conv2d(3, self.in_planes, kernel_size=3, stride=1, padding=1, bias=False)
    self.bn1 = nn.BatchNorm2d(self.in_planes)
    self.layer1 = self._make_layer(block, widths[0], num_blocks[0], stride=1)
    self.layer2 = self._make_layer(block, widths[1], num_blocks[1], stride=2)
    self.layer3 = self._make_layer(block, widths[2], num_blocks[2], stride=2)
    self.layer4 = self._make_layer(block, widths[3], num_blocks[3], stride=2)
    self.linear = nn.Linear(((feat_scale * widths[3]) * block.expansion), num_classes)
