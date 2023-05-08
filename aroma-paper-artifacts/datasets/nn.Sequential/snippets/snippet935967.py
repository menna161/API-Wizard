import math
import torch.nn as nn
from mmdet.ops import DeformConv, ModulatedDeformConv
from .resnet import Bottleneck as _Bottleneck
from .resnet import ResNet
from ..registry import BACKBONES
from ..utils import build_conv_layer, build_norm_layer


def make_res_layer(block, inplanes, planes, blocks, stride=1, dilation=1, groups=1, base_width=4, style='pytorch', with_cp=False, conv_cfg=None, norm_cfg=dict(type='BN'), dcn=None, gcb=None):
    downsample = None
    if ((stride != 1) or (inplanes != (planes * block.expansion))):
        downsample = nn.Sequential(build_conv_layer(conv_cfg, inplanes, (planes * block.expansion), kernel_size=1, stride=stride, bias=False), build_norm_layer(norm_cfg, (planes * block.expansion))[1])
    layers = []
    layers.append(block(inplanes=inplanes, planes=planes, stride=stride, dilation=dilation, downsample=downsample, groups=groups, base_width=base_width, style=style, with_cp=with_cp, conv_cfg=conv_cfg, norm_cfg=norm_cfg, dcn=dcn, gcb=gcb))
    inplanes = (planes * block.expansion)
    for i in range(1, blocks):
        layers.append(block(inplanes=inplanes, planes=planes, stride=1, dilation=dilation, groups=groups, base_width=base_width, style=style, with_cp=with_cp, conv_cfg=conv_cfg, norm_cfg=norm_cfg, dcn=dcn, gcb=gcb))
    return nn.Sequential(*layers)
