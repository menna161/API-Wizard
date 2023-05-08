import pytest
import unittest
import torch
import torch_testing as tt
import numpy as np
from gym.spaces import Box
from rlil import nn
from rlil.approximation import FixedTarget
from rlil.environments import State
from rlil.policies import DeterministicPolicy


def setUp(self):
    torch.manual_seed(2)
    self.model = nn.Sequential(nn.Linear0(STATE_DIM, ACTION_DIM))
    self.optimizer = torch.optim.RMSprop(self.model.parameters(), lr=0.01)
    self.space = Box(np.array([(- 1), (- 1), (- 1)]), np.array([1, 1, 1]), dtype=np.float32)
    self.policy = DeterministicPolicy(self.model, self.optimizer, self.space)
