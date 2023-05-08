import unittest
import numpy as np
import torch
from torch import nn
import torch_testing as tt
from gym.spaces import Box
from rlil.environments import State
from rlil.policies import GaussianPolicy


def setUp(self):
    torch.manual_seed(2)
    self.space = Box(np.array([(- 1), (- 1), (- 1)]), np.array([1, 1, 1]))
    self.model = nn.Sequential(nn.Linear(STATE_DIM, (ACTION_DIM * 2)))
    optimizer = torch.optim.RMSprop(self.model.parameters(), lr=0.01)
    self.policy = GaussianPolicy(self.model, optimizer, self.space)
