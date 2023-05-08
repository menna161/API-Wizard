from __future__ import print_function, division, absolute_import
import torch.nn as nn
from seg_opr.seg_oprs import ConvBnRelu
from utils.pyt_utils import load_model


def __init__(self, in_channels, mid_out_channels, has_proj, stride, dilation=1, norm_layer=nn.BatchNorm2d):
    super(Block, self).__init__()
    self.has_proj = has_proj
    if has_proj:
        self.proj = SeparableConvBnRelu(in_channels, (mid_out_channels * self.expansion), 3, stride, 1, has_relu=False, norm_layer=norm_layer)
    self.residual_branch = nn.Sequential(SeparableConvBnRelu(in_channels, mid_out_channels, 3, stride, dilation, dilation, has_relu=True, norm_layer=norm_layer), SeparableConvBnRelu(mid_out_channels, mid_out_channels, 3, 1, 1, has_relu=True, norm_layer=norm_layer), SeparableConvBnRelu(mid_out_channels, (mid_out_channels * self.expansion), 3, 1, 1, has_relu=False, norm_layer=norm_layer))
    self.relu = nn.ReLU(inplace=True)
