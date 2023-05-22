from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import torch
import math
from torch import nn
from torch.nn.modules.utils import _pair
from .dcn_v2_func import DCNv2Function
from .dcn_v2_func import DCNv2PoolingFunction


def __init__(self, spatial_scale, pooled_size, output_dim, no_trans, group_size=1, part_size=None, sample_per_part=4, trans_std=0.0, deform_fc_dim=1024):
    super(DCNPooling, self).__init__(spatial_scale, pooled_size, output_dim, no_trans, group_size, part_size, sample_per_part, trans_std)
    self.deform_fc_dim = deform_fc_dim
    if (not no_trans):
        self.func_offset = DCNv2PoolingFunction(self.spatial_scale, self.pooled_size, self.output_dim, True, self.group_size, self.part_size, self.sample_per_part, self.trans_std)
        self.offset_fc = nn.Sequential(nn.Linear(((self.pooled_size * self.pooled_size) * self.output_dim), self.deform_fc_dim), nn.ReLU(inplace=True), nn.Linear(self.deform_fc_dim, self.deform_fc_dim), nn.ReLU(inplace=True), nn.Linear(self.deform_fc_dim, ((self.pooled_size * self.pooled_size) * 2)))
        self.offset_fc[4].weight.data.zero_()
        self.offset_fc[4].bias.data.zero_()
        self.mask_fc = nn.Sequential(nn.Linear(((self.pooled_size * self.pooled_size) * self.output_dim), self.deform_fc_dim), nn.ReLU(inplace=True), nn.Linear(self.deform_fc_dim, ((self.pooled_size * self.pooled_size) * 1)), nn.Sigmoid())
        self.mask_fc[2].weight.data.zero_()
        self.mask_fc[2].bias.data.zero_()
