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


def check_pooling_zero_offset():
    from dcn_v2 import DCNv2Pooling
    input = torch.randn(2, 16, 64, 64).cuda().zero_()
    input[(0, :, 16:26, 16:26)] = 1.0
    input[(1, :, 10:20, 20:30)] = 2.0
    rois = torch.tensor([[0, 65, 65, 103, 103], [1, 81, 41, 119, 79]]).cuda().float()
    pooling = DCNv2Pooling(spatial_scale=(1.0 / 4), pooled_size=7, output_dim=16, no_trans=True, group_size=1, trans_std=0.1).cuda()
    out = pooling(input, rois, input.new())
    s = ', '.join([('%f' % out[(i, :, :, :)].mean().item()) for i in range(rois.shape[0])])
    print(s)
    dpooling = DCNv2Pooling(spatial_scale=(1.0 / 4), pooled_size=7, output_dim=16, no_trans=False, group_size=1, trans_std=0.1).cuda()
    offset = torch.randn(20, 2, 7, 7).cuda().zero_()
    dout = dpooling(input, rois, offset)
    s = ', '.join([('%f' % dout[(i, :, :, :)].mean().item()) for i in range(rois.shape[0])])
    print(s)
