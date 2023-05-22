import torch
from torch import nn
from torch.nn import init
import torch.nn.functional as F
import math
from torch.autograd import Variable
import numpy as np
from .deeplab_resnet import resnet50_locate
from .vgg import vgg16_locate


def __init__(self, k_in, k_out_list):
    super(BlockLayer, self).__init__()
    (up_in1, up_mid1, up_in2, up_mid2, up_out) = ([], [], [], [], [])
    for k in k_out_list:
        up_in1.append(nn.Conv2d(k_in, (k_in // 4), 1, 1, bias=False))
        up_mid1.append(nn.Sequential(nn.Conv2d((k_in // 4), (k_in // 4), 3, 1, 1, bias=False), nn.Conv2d((k_in // 4), k_in, 1, 1, bias=False)))
        up_in2.append(nn.Conv2d(k_in, (k_in // 4), 1, 1, bias=False))
        up_mid2.append(nn.Sequential(nn.Conv2d((k_in // 4), (k_in // 4), 3, 1, 1, bias=False), nn.Conv2d((k_in // 4), k_in, 1, 1, bias=False)))
        up_out.append(nn.Conv2d(k_in, k, 1, 1, bias=False))
    self.block_in1 = nn.ModuleList(up_in1)
    self.block_in2 = nn.ModuleList(up_in2)
    self.block_mid1 = nn.ModuleList(up_mid1)
    self.block_mid2 = nn.ModuleList(up_mid2)
    self.block_out = nn.ModuleList(up_out)
    self.relu = nn.ReLU()
