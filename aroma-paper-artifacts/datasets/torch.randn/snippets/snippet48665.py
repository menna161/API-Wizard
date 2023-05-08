from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import time
import torch
import torch.nn as nn
from torch.autograd import gradcheck
from dcn_v2 import DCNv2
from dcn_v2_func import DCNv2Function
from dcn_v2 import DCNv2Pooling
from dcn_v2_func import DCNv2PoolingFunction
from dcn_v2 import DCNv2Pooling
from dcn_v2 import DCN
from dcn_v2 import DCNv2Pooling
from dcn_v2 import DCNPooling


def check_gradient_dpooling():
    input = (torch.randn(2, 3, 5, 5).cuda() * 0.01)
    N = 4
    batch_inds = torch.randint(2, (N, 1)).cuda().float()
    x = (torch.rand((N, 1)).cuda().float() * 15)
    y = (torch.rand((N, 1)).cuda().float() * 15)
    w = (torch.rand((N, 1)).cuda().float() * 10)
    h = (torch.rand((N, 1)).cuda().float() * 10)
    rois = torch.cat((batch_inds, x, y, (x + w), (y + h)), dim=1)
    offset = torch.randn(N, 2, 3, 3).cuda()
    dpooling = DCNv2Pooling(spatial_scale=(1.0 / 4), pooled_size=3, output_dim=3, no_trans=False, group_size=1, trans_std=0.0).cuda()
    input.requires_grad = True
    offset.requires_grad = True
    print('check_gradient_dpooling', gradcheck(dpooling, (input, rois, offset), eps=0.0001))
