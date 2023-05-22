import unittest
import numpy as np
import torch
from torch import nn
import torch_testing as tt
from gym.spaces import Box
from rlil.environments import State
from rlil.policies import GaussianPolicy


def test_reinforce_one(self):
    state = State(torch.randn(1, STATE_DIM))
    dist = self.policy(state)
    action = dist.sample()
    log_prob1 = dist.log_prob(action)
    loss = (- log_prob1.mean())
    self.policy.reinforce(loss)
    dist = self.policy(state)
    log_prob2 = dist.log_prob(action)
    self.assertGreater(log_prob2.item(), log_prob1.item())
