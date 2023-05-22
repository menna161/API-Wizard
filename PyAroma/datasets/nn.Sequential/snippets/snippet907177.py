import torch
import torch.nn as nn
from lib.ssn.ssn import ssn_iter, sparse_ssn_iter


def conv_bn_relu(in_c, out_c):
    return nn.Sequential(nn.Conv2d(in_c, out_c, 3, padding=1, bias=False), nn.BatchNorm2d(out_c), nn.ReLU(True))
