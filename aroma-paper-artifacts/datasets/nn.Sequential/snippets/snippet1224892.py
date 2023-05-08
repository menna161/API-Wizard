from __future__ import print_function, division, absolute_import
import torch.nn as nn
from seg_opr.seg_oprs import ConvBnRelu
from utils.pyt_utils import load_model


def _make_layer(self, block, norm_layer, blocks, mid_out_channels, stride=1):
    layers = []
    has_proj = (True if (stride > 1) else False)
    layers.append(block(self.in_channels, mid_out_channels, has_proj, stride=stride, norm_layer=norm_layer))
    self.in_channels = (mid_out_channels * block.expansion)
    for i in range(1, blocks):
        layers.append(block(self.in_channels, mid_out_channels, has_proj=False, stride=1, norm_layer=norm_layer))
    return nn.Sequential(*layers)
