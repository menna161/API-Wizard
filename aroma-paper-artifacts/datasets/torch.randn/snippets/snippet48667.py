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


def example_dpooling():
    from dcn_v2 import DCNv2Pooling
    input = torch.randn(2, 32, 64, 64).cuda()
    batch_inds = torch.randint(2, (20, 1)).cuda().float()
    x = torch.randint(256, (20, 1)).cuda().float()
    y = torch.randint(256, (20, 1)).cuda().float()
    w = torch.randint(64, (20, 1)).cuda().float()
    h = torch.randint(64, (20, 1)).cuda().float()
    rois = torch.cat((batch_inds, x, y, (x + w), (y + h)), dim=1)
    offset = torch.randn(20, 2, 7, 7).cuda()
    input.requires_grad = True
    offset.requires_grad = True
    pooling = DCNv2Pooling(spatial_scale=(1.0 / 4), pooled_size=7, output_dim=32, no_trans=True, group_size=1, trans_std=0.1).cuda()
    dpooling = DCNv2Pooling(spatial_scale=(1.0 / 4), pooled_size=7, output_dim=32, no_trans=False, group_size=1, trans_std=0.1).cuda()
    out = pooling(input, rois, offset)
    dout = dpooling(input, rois, offset)
    print(out.shape)
    print(dout.shape)
    target_out = out.new(*out.size())
    target_out.data.uniform_((- 0.01), 0.01)
    target_dout = dout.new(*dout.size())
    target_dout.data.uniform_((- 0.01), 0.01)
    e = (target_out - out).mean()
    e.backward()
    e = (target_dout - dout).mean()
    e.backward()
