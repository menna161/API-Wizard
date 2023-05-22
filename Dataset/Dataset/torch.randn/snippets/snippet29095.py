import torch
import torch.nn as nn
from nbdt.loss import SoftTreeSupLoss, HardTreeSupLoss
from nbdt.model import HardNBDT


def test_criterion_tinyimagenet200(criterion):
    criterion = SoftTreeSupLoss(dataset='TinyImagenet200', criterion=criterion, hierarchy='induced')
    criterion(torch.randn((1, 200)), torch.randint(200, (1,)))
