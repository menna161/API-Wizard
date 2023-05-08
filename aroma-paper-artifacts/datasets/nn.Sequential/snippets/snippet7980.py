import os
import sys
from public.path import pretrained_models_path
import torch
import torch.nn as nn
import torch.nn.functional as F


def _make_stage(self, layer_config, num_inchannels, multi_scale_output=True):
    num_modules = layer_config['NUM_MODULES']
    num_branches = layer_config['NUM_BRANCHES']
    num_blocks = layer_config['NUM_BLOCKS']
    num_channels = layer_config['NUM_CHANNELS']
    block = blocks_dict[layer_config['BLOCK']]
    fuse_method = layer_config['FUSE_METHOD']
    modules = []
    for i in range(num_modules):
        if ((not multi_scale_output) and (i == (num_modules - 1))):
            reset_multi_scale_output = False
        else:
            reset_multi_scale_output = True
        modules.append(HighResolutionModule(num_branches, block, num_blocks, num_inchannels, num_channels, fuse_method, reset_multi_scale_output))
        num_inchannels = modules[(- 1)].get_num_inchannels()
    return (nn.Sequential(*modules), num_inchannels)
