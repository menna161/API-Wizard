import logging
import torch.nn as nn
from mmcv.cnn import constant_init, kaiming_init
from mmcv.runner import load_checkpoint
from torch.nn.modules.batchnorm import _BatchNorm
from ..registry import BACKBONES
from ..utils import build_norm_layer, build_conv_layer
from .resnet import BasicBlock, Bottleneck


def _make_layer(self, block, inplanes, planes, blocks, stride=1):
    downsample = None
    if ((stride != 1) or (inplanes != (planes * block.expansion))):
        downsample = nn.Sequential(build_conv_layer(self.conv_cfg, inplanes, (planes * block.expansion), kernel_size=1, stride=stride, bias=False), build_norm_layer(self.norm_cfg, (planes * block.expansion))[1])
    layers = []
    layers.append(block(inplanes, planes, stride, downsample=downsample, with_cp=self.with_cp, norm_cfg=self.norm_cfg, conv_cfg=self.conv_cfg))
    inplanes = (planes * block.expansion)
    for i in range(1, blocks):
        layers.append(block(inplanes, planes, with_cp=self.with_cp, norm_cfg=self.norm_cfg, conv_cfg=self.conv_cfg))
    return nn.Sequential(*layers)
