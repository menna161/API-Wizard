from collections import OrderedDict
import numpy as np
import torch
import torch.nn as nn


def __init__(self, in_planes, out_planes, norm_layer=nn.BatchNorm2d):
    super(AttentionRefinement, self).__init__()
    self.conv_3x3 = ConvBnRelu(in_planes, out_planes, 3, 1, 1, has_bn=True, norm_layer=norm_layer, has_relu=True, has_bias=False)
    self.channel_attention = nn.Sequential(nn.AdaptiveAvgPool2d(1), ConvBnRelu(out_planes, out_planes, 1, 1, 0, has_bn=True, norm_layer=norm_layer, has_relu=False, has_bias=False), nn.Sigmoid())
