import torch.nn as nn
from mmcv.cnn import constant_init, kaiming_init
from mmcv.runner import load_checkpoint
from torch.nn.modules.batchnorm import _BatchNorm
from mmdet.ops import build_conv_layer, build_norm_layer
from mmdet.utils import get_root_logger
from ..registry import BACKBONES
from .resnet import BasicBlock, Bottleneck


def _make_one_branch(self, branch_index, block, num_blocks, num_channels, stride=1):
    downsample = None
    if ((stride != 1) or (self.in_channels[branch_index] != (num_channels[branch_index] * block.expansion))):
        downsample = nn.Sequential(build_conv_layer(self.conv_cfg, self.in_channels[branch_index], (num_channels[branch_index] * block.expansion), kernel_size=1, stride=stride, bias=False), build_norm_layer(self.norm_cfg, (num_channels[branch_index] * block.expansion))[1])
    layers = []
    layers.append(block(self.in_channels[branch_index], num_channels[branch_index], stride, downsample=downsample, with_cp=self.with_cp, norm_cfg=self.norm_cfg, conv_cfg=self.conv_cfg))
    self.in_channels[branch_index] = (num_channels[branch_index] * block.expansion)
    for i in range(1, num_blocks[branch_index]):
        layers.append(block(self.in_channels[branch_index], num_channels[branch_index], with_cp=self.with_cp, norm_cfg=self.norm_cfg, conv_cfg=self.conv_cfg))
    return nn.Sequential(*layers)
