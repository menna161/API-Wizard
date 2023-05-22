import unittest
import numpy as np
import torch
from torch import nn
import torch_testing as tt
from gym.spaces import Box
from rlil.environments import State
from rlil.policies import GaussianPolicy


def test_converge(self):
    state = State(torch.randn(1, STATE_DIM))
    target = torch.tensor([1.0, 2.0, (- 1.0)])
    for _ in range(0, 1000):
        dist = self.policy(state)
        action = dist.sample()
        log_prob = dist.log_prob(action)
        error = ((target - action) ** 2).mean()
        loss = (error * log_prob).mean()
        self.policy.reinforce(loss)
    self.assertTrue((error < 1))
