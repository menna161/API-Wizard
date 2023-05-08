import unittest
import torch
from torch import nn
import torch_testing as tt
from rlil.environments import State
from rlil.policies import SoftmaxPolicy


def setUp(self):
    torch.manual_seed(2)
    self.model = nn.Sequential(nn.Linear(STATE_DIM, ACTIONS))
    optimizer = torch.optim.SGD(self.model.parameters(), lr=0.1)
    self.policy = SoftmaxPolicy(self.model, optimizer)
