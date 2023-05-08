import torch.nn as nn
import math
import torch.utils.model_zoo as model_zoo
from networks.deeplab.sync_batchnorm.batchnorm import SynchronizedBatchNorm2d
import torch


def __init__(self, block, layers, arch='D', channels=(16, 32, 64, 128, 256, 512, 512, 512), BatchNorm=None):
    super(DRN, self).__init__()
    self.inplanes = channels[0]
    self.out_dim = channels[(- 1)]
    self.arch = arch
    if (arch == 'C'):
        self.conv1 = nn.Conv2d(3, channels[0], kernel_size=7, stride=1, padding=3, bias=False)
        self.bn1 = BatchNorm(channels[0])
        self.relu = nn.ReLU(inplace=True)
        self.layer1 = self._make_layer(BasicBlock, channels[0], layers[0], stride=1, BatchNorm=BatchNorm)
        self.layer2 = self._make_layer(BasicBlock, channels[1], layers[1], stride=2, BatchNorm=BatchNorm)
    elif (arch == 'D'):
        self.layer0 = nn.Sequential(nn.Conv2d(3, channels[0], kernel_size=7, stride=1, padding=3, bias=False), BatchNorm(channels[0]), nn.ReLU(inplace=True))
        self.layer1 = self._make_conv_layers(channels[0], layers[0], stride=1, BatchNorm=BatchNorm)
        self.layer2 = self._make_conv_layers(channels[1], layers[1], stride=2, BatchNorm=BatchNorm)
    self.layer3 = self._make_layer(block, channels[2], layers[2], stride=2, BatchNorm=BatchNorm)
    self.layer4 = self._make_layer(block, channels[3], layers[3], stride=2, BatchNorm=BatchNorm)
    self.layer5 = self._make_layer(block, channels[4], layers[4], dilation=2, new_level=False, BatchNorm=BatchNorm)
    self.layer6 = (None if (layers[5] == 0) else self._make_layer(block, channels[5], layers[5], dilation=4, new_level=False, BatchNorm=BatchNorm))
    if (arch == 'C'):
        self.layer7 = (None if (layers[6] == 0) else self._make_layer(BasicBlock, channels[6], layers[6], dilation=2, new_level=False, residual=False, BatchNorm=BatchNorm))
        self.layer8 = (None if (layers[7] == 0) else self._make_layer(BasicBlock, channels[7], layers[7], dilation=1, new_level=False, residual=False, BatchNorm=BatchNorm))
    elif (arch == 'D'):
        self.layer7 = (None if (layers[6] == 0) else self._make_conv_layers(channels[6], layers[6], dilation=2, BatchNorm=BatchNorm))
        self.layer8 = (None if (layers[7] == 0) else self._make_conv_layers(channels[7], layers[7], dilation=1, BatchNorm=BatchNorm))
    self._init_weight()
