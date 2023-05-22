import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.model_zoo as model_zoo
from collections import OrderedDict


def __init__(self, small=False, num_init_features=64, k_r=96, groups=32, b=False, k_sec=(3, 4, 20, 3), inc_sec=(16, 32, 24, 128), num_classes=1000, test_time_pool=False):
    super(DPN, self).__init__()
    self.test_time_pool = test_time_pool
    self.b = b
    bw_factor = (1 if small else 4)
    self.k_sec = k_sec
    self.out_channels = []
    self.blocks = OrderedDict()
    if small:
        self.blocks['conv1_1'] = InputBlock(num_init_features, kernel_size=3, padding=1)
    else:
        self.blocks['conv1_1'] = InputBlock(num_init_features, kernel_size=7, padding=3)
    self.out_channels.append(num_init_features)
    bw = (64 * bw_factor)
    inc = inc_sec[0]
    r = ((k_r * bw) // (64 * bw_factor))
    self.blocks['conv2_1'] = DualPathBlock(num_init_features, r, r, bw, inc, groups, 'proj', b)
    in_chs = (bw + (3 * inc))
    for i in range(2, (k_sec[0] + 1)):
        self.blocks[('conv2_' + str(i))] = DualPathBlock(in_chs, r, r, bw, inc, groups, 'normal', b)
        in_chs += inc
    self.out_channels.append(in_chs)
    bw = (128 * bw_factor)
    inc = inc_sec[1]
    r = ((k_r * bw) // (64 * bw_factor))
    self.blocks['conv3_1'] = DualPathBlock(in_chs, r, r, bw, inc, groups, 'down', b)
    in_chs = (bw + (3 * inc))
    for i in range(2, (k_sec[1] + 1)):
        self.blocks[('conv3_' + str(i))] = DualPathBlock(in_chs, r, r, bw, inc, groups, 'normal', b)
        in_chs += inc
    self.out_channels.append(in_chs)
    bw = (256 * bw_factor)
    inc = inc_sec[2]
    r = ((k_r * bw) // (64 * bw_factor))
    self.blocks['conv4_1'] = DualPathBlock(in_chs, r, r, bw, inc, groups, 'down', b)
    in_chs = (bw + (3 * inc))
    for i in range(2, (k_sec[2] + 1)):
        self.blocks[('conv4_' + str(i))] = DualPathBlock(in_chs, r, r, bw, inc, groups, 'normal', b)
        in_chs += inc
    self.out_channels.append(in_chs)
    bw = (512 * bw_factor)
    inc = inc_sec[3]
    r = ((k_r * bw) // (64 * bw_factor))
    self.blocks['conv5_1'] = DualPathBlock(in_chs, r, r, bw, inc, groups, 'down', b)
    in_chs = (bw + (3 * inc))
    for i in range(2, (k_sec[3] + 1)):
        self.blocks[('conv5_' + str(i))] = DualPathBlock(in_chs, r, r, bw, inc, groups, 'normal', b)
        in_chs += inc
    self.blocks['conv5_bn_ac'] = CatBnAct(in_chs)
    self.out_channels.append(in_chs)
    self.features = nn.Sequential(self.blocks)
    self.classifier = nn.Conv2d(in_chs, num_classes, kernel_size=1, bias=True)
