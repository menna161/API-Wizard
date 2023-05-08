import torch
from torch import nn
from torch.nn import init
import torch.nn.functional as F
import math
from torch.autograd import Variable
import numpy as np
from .deeplab_resnet import resnet50_locate
from .vgg import vgg16_locate


def __init__(self, list_k):
    super(ConvertLayer, self).__init__()
    up = []
    for i in range(len(list_k[0])):
        up.append(nn.Sequential(nn.Conv2d(list_k[0][i], list_k[1][i], 1, 1, bias=False), nn.ReLU(inplace=True)))
    self.convert0 = nn.ModuleList(up)
