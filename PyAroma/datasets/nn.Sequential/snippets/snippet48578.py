from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import torch
import torch.nn as nn
from .py_utils import TopPool, BottomPool, LeftPool, RightPool


def __init__(self, n, nstack, dims, modules, heads, pre=None, cnv_dim=256, make_tl_layer=None, make_br_layer=None, make_ct_layer=None, make_cnv_layer=make_cnv_layer, make_heat_layer=make_kp_layer, make_tag_layer=make_kp_layer, make_regr_layer=make_kp_layer, make_up_layer=make_layer, make_low_layer=make_layer, make_hg_layer=make_layer, make_hg_layer_revr=make_layer_revr, make_pool_layer=make_pool_layer, make_unpool_layer=make_unpool_layer, make_merge_layer=make_merge_layer, make_inter_layer=make_inter_layer, kp_layer=residual):
    super(exkp, self).__init__()
    self.nstack = nstack
    self.heads = heads
    curr_dim = dims[0]
    self.pre = (nn.Sequential(convolution(7, 3, 128, stride=2), residual(3, 128, 256, stride=2)) if (pre is None) else pre)
    self.kps = nn.ModuleList([kp_module(n, dims, modules, layer=kp_layer, make_up_layer=make_up_layer, make_low_layer=make_low_layer, make_hg_layer=make_hg_layer, make_hg_layer_revr=make_hg_layer_revr, make_pool_layer=make_pool_layer, make_unpool_layer=make_unpool_layer, make_merge_layer=make_merge_layer) for _ in range(nstack)])
    self.cnvs = nn.ModuleList([make_cnv_layer(curr_dim, cnv_dim) for _ in range(nstack)])
    self.ct_cnvs = nn.ModuleList([make_ct_layer(cnv_dim) for _ in range(nstack)])
    self.inters = nn.ModuleList([make_inter_layer(curr_dim) for _ in range((nstack - 1))])
    self.inters_ = nn.ModuleList([nn.Sequential(nn.Conv2d(curr_dim, curr_dim, (1, 1), bias=False), nn.BatchNorm2d(curr_dim)) for _ in range((nstack - 1))])
    self.cnvs_ = nn.ModuleList([nn.Sequential(nn.Conv2d(cnv_dim, curr_dim, (1, 1), bias=False), nn.BatchNorm2d(curr_dim)) for _ in range((nstack - 1))])
    for head in heads.keys():
        if ('hm' or 'hm_act_f' or ('wh_act' in head)):
            module = nn.ModuleList([make_heat_layer(cnv_dim, curr_dim, heads[head]) for _ in range(nstack)])
            self.__setattr__(head, module)
            for heat in self.__getattr__(head):
                heat[(- 1)].bias.data.fill_((- 2.19))
        else:
            module = nn.ModuleList([make_regr_layer(cnv_dim, curr_dim, heads[head]) for _ in range(nstack)])
            self.__setattr__(head, module)
    self.relu = nn.ReLU(inplace=True)
