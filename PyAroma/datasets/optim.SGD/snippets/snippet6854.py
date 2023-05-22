import unittest
import torch
from torch import nn
import torch_testing as tt
from rlil.approximation.v_network import VNetwork
from rlil.environments import State


def setUp(self):
    torch.manual_seed(2)
    self.model = nn.Sequential(nn.Linear(STATE_DIM, 1))
    optimizer = torch.optim.SGD(self.model.parameters(), lr=0.1)
    self.v = VNetwork(self.model, optimizer)
