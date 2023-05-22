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


def check_gradient_dconv_double():
    input = torch.randn(N, inC, inH, inW, dtype=torch.float64).cuda()
    input.requires_grad = True
    offset = torch.randn(N, (((deformable_groups * 2) * kW) * kH), inH, inW, dtype=torch.float64).cuda()
    offset.requires_grad = True
    mask = torch.rand(N, (((deformable_groups * 1) * kW) * kH), inH, inW, dtype=torch.float64).cuda()
    mask.requires_grad = True
    mask = torch.sigmoid(mask)
    weight = torch.randn(outC, inC, kH, kW, dtype=torch.float64).cuda()
    weight.requires_grad = True
    bias = torch.rand(outC, dtype=torch.float64).cuda()
    bias.requires_grad = True
    func = DCNv2Function(stride=1, padding=1, dilation=1, deformable_groups=deformable_groups)
    print(gradcheck(func, (input, offset, mask, weight, bias), eps=1e-06, atol=1e-05, rtol=0.001))
