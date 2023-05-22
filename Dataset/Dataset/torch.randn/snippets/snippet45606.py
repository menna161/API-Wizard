import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable


def test_focal_loss():
    loss = FocalLoss()
    input = Variable(torch.randn(3, 5), requires_grad=True)
    target = Variable(torch.LongTensor(3).random_(5))
    print(input)
    print(target)
    output = loss(input, target)
    print(output)
    output.backward()
