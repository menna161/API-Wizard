from collections import OrderedDict
import numpy as np
import torch
import torch.nn as nn


def __init__(self, in_planes, out_planes, reduction=1, norm_layer=nn.BatchNorm2d):
    super(FeatureFusion, self).__init__()
    self.conv_1x1 = ConvBnRelu(in_planes, out_planes, 1, 1, 0, has_bn=True, norm_layer=norm_layer, has_relu=True, has_bias=False)
    self.channel_attention = nn.Sequential(nn.AdaptiveAvgPool2d(1), ConvBnRelu(out_planes, (out_planes // reduction), 1, 1, 0, has_bn=False, norm_layer=norm_layer, has_relu=True, has_bias=False), ConvBnRelu((out_planes // reduction), out_planes, 1, 1, 0, has_bn=False, norm_layer=norm_layer, has_relu=False, has_bias=False), nn.Sigmoid())
