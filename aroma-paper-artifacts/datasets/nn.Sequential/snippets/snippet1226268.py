import torch.nn as nn
import math
import torch.utils.model_zoo as model_zoo
from networks.deeplab.sync_batchnorm.batchnorm import SynchronizedBatchNorm2d
import torch


def _make_layer(self, block, planes, blocks, stride=1, dilation=1, BatchNorm=None):
    downsample = None
    if ((stride != 1) or (self.inplanes != (planes * block.expansion))):
        downsample = nn.Sequential(nn.Conv2d(self.inplanes, (planes * block.expansion), kernel_size=1, stride=stride, bias=False), BatchNorm((planes * block.expansion)))
    layers = []
    layers.append(block(self.inplanes, planes, stride, downsample, BatchNorm=BatchNorm))
    self.inplanes = (planes * block.expansion)
    for i in range(1, blocks):
        layers.append(block(self.inplanes, planes, dilation=(dilation, dilation), BatchNorm=BatchNorm))
    return nn.Sequential(*layers)
