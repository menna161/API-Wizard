from __future__ import absolute_import
from torch import nn
from torch.autograd import Variable
from torch.nn import functional as F
from torch.nn import init
import torch
import torchvision
import math
from .resnet import *


def __init__(self, input_feature_size, embeding_fea_size=1024, dropout=0.5):
    super(self.__class__, self).__init__()
    self.embeding_fea_size = embeding_fea_size
    self.embeding = nn.Linear(input_feature_size, embeding_fea_size)
    self.embeding_bn = nn.BatchNorm1d(embeding_fea_size)
    init.kaiming_normal_(self.embeding.weight, mode='fan_out')
    init.constant_(self.embeding.bias, 0)
    init.constant_(self.embeding_bn.weight, 1)
    init.constant_(self.embeding_bn.bias, 0)
    self.drop = nn.Dropout(dropout)
