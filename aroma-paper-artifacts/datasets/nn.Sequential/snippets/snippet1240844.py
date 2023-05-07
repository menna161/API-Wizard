import torch
import torch.nn as nn
from torch.autograd import Function
from torch.autograd.function import once_differentiable
from torch.nn.modules.utils import _pair
from . import deform_pool_cuda


def __init__(self, spatial_scale, out_size, out_channels, no_trans, group_size=1, part_size=None, sample_per_part=4, trans_std=0.0, num_offset_fcs=3, deform_fc_channels=1024):
    super(DeformRoIPoolingPack, self).__init__(spatial_scale, out_size, out_channels, no_trans, group_size, part_size, sample_per_part, trans_std)
    self.num_offset_fcs = num_offset_fcs
    self.deform_fc_channels = deform_fc_channels
    if (not no_trans):
        seq = []
        ic = ((self.out_size[0] * self.out_size[1]) * self.out_channels)
        for i in range(self.num_offset_fcs):
            if (i < (self.num_offset_fcs - 1)):
                oc = self.deform_fc_channels
            else:
                oc = ((self.out_size[0] * self.out_size[1]) * 2)
            seq.append(nn.Linear(ic, oc))
            ic = oc
            if (i < (self.num_offset_fcs - 1)):
                seq.append(nn.ReLU(inplace=True))
        self.offset_fc = nn.Sequential(*seq)
        self.offset_fc[(- 1)].weight.data.zero_()
        self.offset_fc[(- 1)].bias.data.zero_()
