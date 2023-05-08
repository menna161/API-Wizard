import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models
import collections
import math
import sys
import Utils
from Utils.CubePad import CustomPad
from . import resnet
import resnet


def __init__(self, in_channels, kernel_size):
    assert (kernel_size >= 2), 'kernel_size out of range: {}'.format(kernel_size)
    super(DeConv, self).__init__()

    def convt(in_channels):
        stride = 2
        padding = ((kernel_size - 1) // 2)
        output_padding = (kernel_size % 2)
        assert (((((- 2) - (2 * padding)) + kernel_size) + output_padding) == 0), 'deconv parameters incorrect'
        module_name = 'deconv{}'.format(kernel_size)
        return nn.Sequential(collections.OrderedDict([(module_name, nn.ConvTranspose2d(in_channels, (in_channels // 2), kernel_size, stride, padding, output_padding, bias=False)), ('batchnorm', nn.BatchNorm2d((in_channels // 2))), ('relu', nn.ReLU(inplace=True))]))
    self.layer1 = convt(in_channels)
    self.layer2 = convt((in_channels // 2))
    self.layer3 = convt((in_channels // (2 ** 2)))
    self.layer4 = convt((in_channels // (2 ** 3)))
