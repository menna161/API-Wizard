import torch.nn as nn
import math
import torch.utils.model_zoo as model_zoo
import mmd
import torch


def __init__(self, block, layers, num_classes=1000, zero_init_residual=False, groups=1, width_per_group=64, norm_layer=None):
    super(ResNet, self).__init__()
    if (norm_layer is None):
        norm_layer = nn.BatchNorm2d
    self.inplanes = 64
    self.groups = groups
    self.base_width = width_per_group
    self.conv1 = nn.Conv2d(3, self.inplanes, kernel_size=7, stride=2, padding=3, bias=False)
    self.bn1 = norm_layer(self.inplanes)
    self.relu = nn.ReLU(inplace=True)
    self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
    self.layer1 = self._make_layer(block, 64, layers[0], norm_layer=norm_layer)
    self.layer2 = self._make_layer(block, 128, layers[1], stride=2, norm_layer=norm_layer)
    self.layer3 = self._make_layer(block, 256, layers[2], stride=2, norm_layer=norm_layer)
    self.layer4 = self._make_layer(block, 512, layers[3], stride=2, norm_layer=norm_layer)
    self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
    self.fc = nn.Linear((512 * block.expansion), num_classes)
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
        elif isinstance(m, (nn.BatchNorm2d, nn.GroupNorm)):
            nn.init.constant_(m.weight, 1)
            nn.init.constant_(m.bias, 0)
    if zero_init_residual:
        for m in self.modules():
            if isinstance(m, Bottleneck):
                nn.init.constant_(m.bn3.weight, 0)
            elif isinstance(m, BasicBlock):
                nn.init.constant_(m.bn2.weight, 0)
