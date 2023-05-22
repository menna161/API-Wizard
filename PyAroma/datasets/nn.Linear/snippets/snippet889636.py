import torch
import torchvision
import torch.nn as nn
from torch.autograd import Variable
import torchvision.models as models
import numpy as np


def foo(net):
    childrens = list(net.children())
    if (not childrens):
        if isinstance(net, torch.nn.Conv2d):
            net.register_forward_hook(conv_hook)
        if isinstance(net, torch.nn.Linear):
            net.register_forward_hook(linear_hook)
        if isinstance(net, torch.nn.BatchNorm2d):
            net.register_forward_hook(bn_hook)
        if isinstance(net, torch.nn.ReLU):
            net.register_forward_hook(relu_hook)
        if (isinstance(net, torch.nn.MaxPool2d) or isinstance(net, torch.nn.AvgPool2d)):
            net.register_forward_hook(pooling_hook)
        return
    for c in childrens:
        foo(c)
