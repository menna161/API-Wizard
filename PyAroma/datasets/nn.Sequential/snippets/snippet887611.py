import torch
from torch import nn
from torch.nn import init
import torch.nn.functional as F
import math
from torch.autograd import Variable
import numpy as np
from .deeplab_resnet import resnet50_locate
from .vgg import vgg16_locate


def __init__(self, k_in, k_out):
    super(EdgeInfoLayerC, self).__init__()
    self.trans = nn.Sequential(nn.Conv2d(k_in, k_in, 3, 1, 1, bias=False), nn.ReLU(inplace=True), nn.Conv2d(k_in, k_out, 3, 1, 1, bias=False), nn.ReLU(inplace=True), nn.Conv2d(k_out, k_out, 3, 1, 1, bias=False), nn.ReLU(inplace=True), nn.Conv2d(k_out, k_out, 3, 1, 1, bias=False), nn.ReLU(inplace=True))
