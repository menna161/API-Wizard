import torch
import torch.nn as nn
import os
from util.download_from_url import download_from_url
from torch.hub import _get_torch_home


def __init__(self, block, layers, num_classes=1000, zero_init_residual=False, norm_layer=None, dropout_prob0=0.0):
    super(PyConvHGResNet, self).__init__()
    if (norm_layer is None):
        norm_layer = nn.BatchNorm2d
    self.inplanes = 64
    self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
    self.bn1 = norm_layer(64)
    self.relu = nn.ReLU(inplace=True)
    self.layer1 = self._make_layer(block, (64 * 2), layers[0], stride=2, norm_layer=norm_layer, pyconv_kernels=[3, 5, 7, 9], pyconv_groups=[32, 32, 32, 32])
    self.layer2 = self._make_layer(block, (128 * 2), layers[1], stride=2, norm_layer=norm_layer, pyconv_kernels=[3, 5, 7], pyconv_groups=[32, 64, 64])
    self.layer3 = self._make_layer(block, (256 * 2), layers[2], stride=2, norm_layer=norm_layer, pyconv_kernels=[3, 5], pyconv_groups=[32, 64])
    self.layer4 = self._make_layer(block, (512 * 2), layers[3], stride=2, norm_layer=norm_layer, pyconv_kernels=[3], pyconv_groups=[32])
    self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
    if (dropout_prob0 > 0.0):
        self.dp = nn.Dropout(dropout_prob0, inplace=True)
        print('Using Dropout with the prob to set to 0 of: ', dropout_prob0)
    else:
        self.dp = None
    self.fc = nn.Linear(((512 * 2) * block.expansion), num_classes)
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
        elif isinstance(m, (nn.BatchNorm2d, nn.GroupNorm)):
            nn.init.constant_(m.weight, 1)
            nn.init.constant_(m.bias, 0)
    if zero_init_residual:
        for m in self.modules():
            if isinstance(m, PyConvBlock):
                nn.init.constant_(m.bn3.weight, 0)
