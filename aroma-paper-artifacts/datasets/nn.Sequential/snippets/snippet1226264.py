import torch.nn as nn
import math
import torch.utils.model_zoo as model_zoo
from networks.deeplab.sync_batchnorm.batchnorm import SynchronizedBatchNorm2d
import torch


def _make_conv_layers(self, channels, convs, stride=1, dilation=1, BatchNorm=None):
    modules = []
    for i in range(convs):
        modules.extend([nn.Conv2d(self.inplanes, channels, kernel_size=3, stride=(stride if (i == 0) else 1), padding=dilation, bias=False, dilation=dilation), BatchNorm(channels), nn.ReLU(inplace=True)])
        self.inplanes = channels
    return nn.Sequential(*modules)
