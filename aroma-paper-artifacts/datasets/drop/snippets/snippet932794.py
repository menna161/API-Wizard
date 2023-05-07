from __future__ import absolute_import
from torch import nn
from torch.autograd import Variable
from torch.nn import functional as F
from torch.nn import init
import torch
import torchvision
import math
from .resnet import *


def forward(self, inputs):
    net = inputs.mean(dim=1)
    eval_feas = F.normalize(net, p=2, dim=1)
    net = self.embeding(net)
    net = self.embeding_bn(net)
    net = F.normalize(net, p=2, dim=1)
    net = self.drop(net)
    return (net, eval_feas)
