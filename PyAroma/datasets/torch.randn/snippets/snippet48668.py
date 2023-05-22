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


def example_mdpooling():
    from dcn_v2 import DCNPooling
    input = torch.randn(2, 32, 64, 64).cuda()
    input.requires_grad = True
    batch_inds = torch.randint(2, (20, 1)).cuda().float()
    x = torch.randint(256, (20, 1)).cuda().float()
    y = torch.randint(256, (20, 1)).cuda().float()
    w = torch.randint(64, (20, 1)).cuda().float()
    h = torch.randint(64, (20, 1)).cuda().float()
    rois = torch.cat((batch_inds, x, y, (x + w), (y + h)), dim=1)
    dpooling = DCNPooling(spatial_scale=(1.0 / 4), pooled_size=7, output_dim=32, no_trans=False, group_size=1, trans_std=0.1).cuda()
    dout = dpooling(input, rois)
    target = dout.new(*dout.size())
    target.data.uniform_((- 0.1), 0.1)
    error = (target - dout).mean()
    error.backward()
    print(dout.shape)
