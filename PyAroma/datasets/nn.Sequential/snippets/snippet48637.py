from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import math
import logging
import torch
import torch.nn as nn
from .DCNv2.dcn_v2 import DCN
import torch.utils.model_zoo as model_zoo


def _make_deconv_layer(self, num_layers, num_filters, num_kernels):
    assert (num_layers == len(num_filters)), 'ERROR: num_deconv_layers is different len(num_deconv_filters)'
    assert (num_layers == len(num_kernels)), 'ERROR: num_deconv_layers is different len(num_deconv_filters)'
    layers = []
    for i in range(num_layers):
        (kernel, padding, output_padding) = self._get_deconv_cfg(num_kernels[i], i)
        planes = num_filters[i]
        fc = DCN(self.inplanes, planes, kernel_size=(3, 3), stride=1, padding=1, dilation=1, deformable_groups=1)
        up = nn.ConvTranspose2d(in_channels=planes, out_channels=planes, kernel_size=kernel, stride=2, padding=padding, output_padding=output_padding, bias=self.deconv_with_bias)
        fill_up_weights(up)
        layers.append(fc)
        layers.append(nn.BatchNorm2d(planes, momentum=BN_MOMENTUM))
        layers.append(nn.ReLU(inplace=True))
        layers.append(up)
        layers.append(nn.BatchNorm2d(planes, momentum=BN_MOMENTUM))
        layers.append(nn.ReLU(inplace=True))
        self.inplanes = planes
    return nn.Sequential(*layers)
