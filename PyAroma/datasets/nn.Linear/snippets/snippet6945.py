import pytest
import unittest
import torch
import torch_testing as tt
import numpy as np
from gym.spaces import Box
from rlil import nn
from rlil.approximation import FixedTarget
from rlil.environments import State, Action, squash_action
from rlil.policies import BCQDeterministicPolicy


def setUp(self):
    torch.manual_seed(2)
    self.model = nn.Sequential(nn.Linear0((STATE_DIM + ACTION_DIM), ACTION_DIM))
    self.optimizer = torch.optim.RMSprop(self.model.parameters(), lr=0.01)
    self.space = Box(np.array([(- 1), (- 1), (- 1)]), np.array([1, 1, 1]), dtype=np.float32)
    self.policy = BCQDeterministicPolicy(self.model, self.optimizer, self.space)
    Action.set_action_space(self.space)
