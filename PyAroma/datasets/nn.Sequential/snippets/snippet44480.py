import torch.nn as nn
import torch.utils.model_zoo as model_zoo
from models_lpf import *


def __init__(self, block, layers, num_classes=1000, zero_init_residual=False, groups=1, width_per_group=64, norm_layer=None, filter_size=1, pool_only=True):
    super(ResNet, self).__init__()
    if (norm_layer is None):
        norm_layer = nn.BatchNorm2d
    planes = [int(((width_per_group * groups) * (2 ** i))) for i in range(4)]
    self.inplanes = planes[0]
    if pool_only:
        self.conv1 = nn.Conv2d(3, planes[0], kernel_size=7, stride=2, padding=3, bias=False)
    else:
        self.conv1 = nn.Conv2d(3, planes[0], kernel_size=7, stride=1, padding=3, bias=False)
    self.bn1 = norm_layer(planes[0])
    self.relu = nn.ReLU(inplace=True)
    if pool_only:
        self.maxpool = nn.Sequential(*[nn.MaxPool2d(kernel_size=2, stride=1), Downsample(filt_size=filter_size, stride=2, channels=planes[0])])
    else:
        self.maxpool = nn.Sequential(*[Downsample(filt_size=filter_size, stride=2, channels=planes[0]), nn.MaxPool2d(kernel_size=2, stride=1), Downsample(filt_size=filter_size, stride=2, channels=planes[0])])
    self.layer1 = self._make_layer(block, planes[0], layers[0], groups=groups, norm_layer=norm_layer)
    self.layer2 = self._make_layer(block, planes[1], layers[1], stride=2, groups=groups, norm_layer=norm_layer, filter_size=filter_size)
    self.layer3 = self._make_layer(block, planes[2], layers[2], stride=2, groups=groups, norm_layer=norm_layer, filter_size=filter_size)
    self.layer4 = self._make_layer(block, planes[3], layers[3], stride=2, groups=groups, norm_layer=norm_layer, filter_size=filter_size)
    self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
    self.fc = nn.Linear((planes[3] * block.expansion), num_classes)
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            if ((m.in_channels != m.out_channels) or (m.out_channels != m.groups) or (m.bias is not None)):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
            else:
                print('Not initializing')
        elif isinstance(m, (nn.BatchNorm2d, nn.GroupNorm)):
            nn.init.constant_(m.weight, 1)
            nn.init.constant_(m.bias, 0)
    if zero_init_residual:
        for m in self.modules():
            if isinstance(m, Bottleneck):
                nn.init.constant_(m.bn3.weight, 0)
            elif isinstance(m, BasicBlock):
                nn.init.constant_(m.bn2.weight, 0)
