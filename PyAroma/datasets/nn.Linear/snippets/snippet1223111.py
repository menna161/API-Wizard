import torch
import torch.nn as nn
from torchvision.models.utils import load_state_dict_from_url
from networks.layers.non_linear import NonLinear
from networks.layers.conv_bn import ConvBN


def __init__(self, nc, block, layers, num_classes=1000, zero_init_residual=False, groups=1, width_per_group=64, replace_stride_with_dilation=None):
    super(ResNet, self).__init__()
    self.nc = nc
    self.inplanes = 64
    self.dilation = 1
    if (replace_stride_with_dilation is None):
        replace_stride_with_dilation = [False, False, False]
    if (len(replace_stride_with_dilation) != 3):
        raise ValueError('replace_stride_with_dilation should be None or a 3-element tuple, got {}'.format(replace_stride_with_dilation))
    self.groups = groups
    self.base_width = width_per_group
    self.conv1_bn = ConvBN(nc, 3, self.inplanes, kernel_size=7, stride=2, padding=3)
    self.relu = NonLinear(nc, self.inplanes)
    self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
    self.layer1 = self._make_layer(block, 64, layers[0])
    self.layer2 = self._make_layer(block, 128, layers[1], stride=2, dilate=replace_stride_with_dilation[0])
    self.layer3 = self._make_layer(block, 256, layers[2], stride=2, dilate=replace_stride_with_dilation[1])
    self.layer4 = self._make_layer(block, 512, layers[3], stride=2, dilate=replace_stride_with_dilation[2])
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
