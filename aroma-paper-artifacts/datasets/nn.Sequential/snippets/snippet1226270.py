import torch
import torch.nn.functional as F
import torch.nn as nn
import math
from networks.deeplab.sync_batchnorm.batchnorm import SynchronizedBatchNorm2d
import torch.utils.model_zoo as model_zoo


def conv_bn(inp, oup, stride, BatchNorm):
    return nn.Sequential(nn.Conv2d(inp, oup, 3, stride, 1, bias=False), BatchNorm(oup), nn.ReLU6(inplace=True))
