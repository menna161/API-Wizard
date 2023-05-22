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


def check_zero_offset():
    conv_offset = nn.Conv2d(inC, (((deformable_groups * 2) * kH) * kW), kernel_size=(kH, kW), stride=(1, 1), padding=(1, 1), bias=True).cuda()
    conv_mask = nn.Conv2d(inC, (((deformable_groups * 1) * kH) * kW), kernel_size=(kH, kW), stride=(1, 1), padding=(1, 1), bias=True).cuda()
    dcn_v2 = DCNv2(inC, outC, (kH, kW), stride=1, padding=1, dilation=1, deformable_groups=deformable_groups).cuda()
    conv_offset.weight.data.zero_()
    conv_offset.bias.data.zero_()
    conv_mask.weight.data.zero_()
    conv_mask.bias.data.zero_()
    conv_identify(dcn_v2.weight, dcn_v2.bias)
    input = torch.randn(N, inC, inH, inW).cuda()
    offset = conv_offset(input)
    mask = conv_mask(input)
    mask = torch.sigmoid(mask)
    output = dcn_v2(input, offset, mask)
    output *= 2
    d = (input - output).abs().max()
    if (d < 1e-10):
        print('Zero offset passed')
    else:
        print('Zero offset failed')
