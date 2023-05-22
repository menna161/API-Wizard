import torch
import torch.nn as nn
import torch.nn.functional as F
from nbdt.models.utils import get_pretrained_model


def test():
    net = ResNet18()
    y = net(torch.randn(1, 3, 32, 32))
    print(y.size())
