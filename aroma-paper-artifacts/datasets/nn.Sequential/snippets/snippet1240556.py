import torch.nn as nn
from mmcv.cnn import constant_init, kaiming_init
from mmcv.runner import load_checkpoint
from torch.nn.modules.batchnorm import _BatchNorm
from mmdet.ops import build_conv_layer, build_norm_layer
from mmdet.utils import get_root_logger
from ..registry import BACKBONES
from .resnet import BasicBlock, Bottleneck


def _make_stage(self, layer_config, in_channels, multiscale_output=True):
    num_modules = layer_config['num_modules']
    num_branches = layer_config['num_branches']
    num_blocks = layer_config['num_blocks']
    num_channels = layer_config['num_channels']
    block = self.blocks_dict[layer_config['block']]
    hr_modules = []
    for i in range(num_modules):
        if ((not multiscale_output) and (i == (num_modules - 1))):
            reset_multiscale_output = False
        else:
            reset_multiscale_output = True
        hr_modules.append(HRModule(num_branches, block, num_blocks, in_channels, num_channels, reset_multiscale_output, with_cp=self.with_cp, norm_cfg=self.norm_cfg, conv_cfg=self.conv_cfg))
    return (nn.Sequential(*hr_modules), in_channels)
