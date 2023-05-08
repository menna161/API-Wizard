import torch
import torch.nn as nn
from nbdt.loss import SoftTreeSupLoss, HardTreeSupLoss
from nbdt.model import HardNBDT


def test_criterion_cifar100(criterion):
    criterion = SoftTreeSupLoss(dataset='CIFAR100', criterion=criterion, hierarchy='induced')
    criterion(torch.randn((1, 100)), torch.randint(100, (1,)))
