import unittest
import torch
from torch import nn
import torch_testing as tt
from rlil.environments import State
from rlil.policies import SoftmaxPolicy


def test_list(self):
    torch.manual_seed(1)
    states = State(torch.randn(3, STATE_DIM), torch.tensor([1, 0, 1]))
    dist = self.policy(states)
    actions = dist.sample()
    log_probs = dist.log_prob(actions)
    tt.assert_equal(actions, torch.tensor([1, 2, 1]))
    loss = (- (torch.tensor([[1, 2, 3]]) * log_probs).mean())
    self.policy.reinforce(loss)
