import torch
import torch.nn as nn
from nbdt.loss import SoftTreeSupLoss, HardTreeSupLoss
from nbdt.model import HardNBDT


def test_criterion_cifar10(criterion, label_cifar10):
    criterion = SoftTreeSupLoss(dataset='CIFAR10', criterion=criterion, hierarchy='induced')
    criterion(torch.randn((1, 10)), label_cifar10)
