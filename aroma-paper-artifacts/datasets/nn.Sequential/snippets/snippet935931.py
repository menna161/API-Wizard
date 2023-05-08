import logging
import torch
import torch.nn as nn
import torch.utils.checkpoint as cp
from torch.nn.modules.batchnorm import _BatchNorm
from mmcv.cnn import constant_init, kaiming_init
from mmcv.runner import load_checkpoint
from mmdet.ops import DeformConv, ModulatedDeformConv, ContextBlock
from mmdet.models.plugins import GeneralizedAttention
from ..registry import BACKBONES
from ..utils import build_conv_layer, build_norm_layer


def make_res_layer(block, inplanes, planes, blocks, stride=1, dilation=1, style='pytorch', with_cp=False, conv_cfg=None, norm_cfg=dict(type='BN'), dcn=None, gcb=None, gen_attention=None, gen_attention_blocks=[]):
    downsample = None
    if ((stride != 1) or (inplanes != (planes * block.expansion))):
        downsample = nn.Sequential(build_conv_layer(conv_cfg, inplanes, (planes * block.expansion), kernel_size=1, stride=stride, bias=False), build_norm_layer(norm_cfg, (planes * block.expansion))[1])
    layers = []
    layers.append(block(inplanes=inplanes, planes=planes, stride=stride, dilation=dilation, downsample=downsample, style=style, with_cp=with_cp, conv_cfg=conv_cfg, norm_cfg=norm_cfg, dcn=dcn, gcb=gcb, gen_attention=(gen_attention if (0 in gen_attention_blocks) else None)))
    inplanes = (planes * block.expansion)
    for i in range(1, blocks):
        layers.append(block(inplanes=inplanes, planes=planes, stride=1, dilation=dilation, style=style, with_cp=with_cp, conv_cfg=conv_cfg, norm_cfg=norm_cfg, dcn=dcn, gcb=gcb, gen_attention=(gen_attention if (i in gen_attention_blocks) else None)))
    return nn.Sequential(*layers)
