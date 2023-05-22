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


def example_dconv():
    from dcn_v2 import DCN
    input = torch.randn(2, 64, 128, 128).cuda()
    dcn = DCN(64, 64, kernel_size=(3, 3), stride=1, padding=1, deformable_groups=2).cuda()
    output = dcn(input)
    targert = output.new(*output.size())
    targert.data.uniform_((- 0.01), 0.01)
    error = (targert - output).mean()
    error.backward()
    print(output.shape)
