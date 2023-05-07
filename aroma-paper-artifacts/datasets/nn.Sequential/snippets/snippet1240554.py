import torch.nn as nn
from mmcv.cnn import constant_init, kaiming_init
from mmcv.runner import load_checkpoint
from torch.nn.modules.batchnorm import _BatchNorm
from mmdet.ops import build_conv_layer, build_norm_layer
from mmdet.utils import get_root_logger
from ..registry import BACKBONES
from .resnet import BasicBlock, Bottleneck


def _make_transition_layer(self, num_channels_pre_layer, num_channels_cur_layer):
    num_branches_cur = len(num_channels_cur_layer)
    num_branches_pre = len(num_channels_pre_layer)
    transition_layers = []
    for i in range(num_branches_cur):
        if (i < num_branches_pre):
            if (num_channels_cur_layer[i] != num_channels_pre_layer[i]):
                transition_layers.append(nn.Sequential(build_conv_layer(self.conv_cfg, num_channels_pre_layer[i], num_channels_cur_layer[i], kernel_size=3, stride=1, padding=1, bias=False), build_norm_layer(self.norm_cfg, num_channels_cur_layer[i])[1], nn.ReLU(inplace=True)))
            else:
                transition_layers.append(None)
        else:
            conv_downsamples = []
            for j in range(((i + 1) - num_branches_pre)):
                in_channels = num_channels_pre_layer[(- 1)]
                out_channels = (num_channels_cur_layer[i] if (j == (i - num_branches_pre)) else in_channels)
                conv_downsamples.append(nn.Sequential(build_conv_layer(self.conv_cfg, in_channels, out_channels, kernel_size=3, stride=2, padding=1, bias=False), build_norm_layer(self.norm_cfg, out_channels)[1], nn.ReLU(inplace=True)))
            transition_layers.append(nn.Sequential(*conv_downsamples))
    return nn.ModuleList(transition_layers)
