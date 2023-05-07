import torch.nn as nn
from mmcv.cnn import constant_init, kaiming_init
from mmcv.runner import load_checkpoint
from torch.nn.modules.batchnorm import _BatchNorm
from mmdet.ops import build_conv_layer, build_norm_layer
from mmdet.utils import get_root_logger
from ..registry import BACKBONES
from .resnet import BasicBlock, Bottleneck


def _make_fuse_layers(self):
    if (self.num_branches == 1):
        return None
    num_branches = self.num_branches
    in_channels = self.in_channels
    fuse_layers = []
    num_out_branches = (num_branches if self.multiscale_output else 1)
    for i in range(num_out_branches):
        fuse_layer = []
        for j in range(num_branches):
            if (j > i):
                fuse_layer.append(nn.Sequential(build_conv_layer(self.conv_cfg, in_channels[j], in_channels[i], kernel_size=1, stride=1, padding=0, bias=False), build_norm_layer(self.norm_cfg, in_channels[i])[1], nn.Upsample(scale_factor=(2 ** (j - i)), mode='nearest')))
            elif (j == i):
                fuse_layer.append(None)
            else:
                conv_downsamples = []
                for k in range((i - j)):
                    if (k == ((i - j) - 1)):
                        conv_downsamples.append(nn.Sequential(build_conv_layer(self.conv_cfg, in_channels[j], in_channels[i], kernel_size=3, stride=2, padding=1, bias=False), build_norm_layer(self.norm_cfg, in_channels[i])[1]))
                    else:
                        conv_downsamples.append(nn.Sequential(build_conv_layer(self.conv_cfg, in_channels[j], in_channels[j], kernel_size=3, stride=2, padding=1, bias=False), build_norm_layer(self.norm_cfg, in_channels[j])[1], nn.ReLU(inplace=False)))
                fuse_layer.append(nn.Sequential(*conv_downsamples))
        fuse_layers.append(nn.ModuleList(fuse_layer))
    return nn.ModuleList(fuse_layers)
