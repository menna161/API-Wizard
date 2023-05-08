import unittest
import torch
from torch import nn
import torch_testing as tt
from rlil.environments import State
from rlil.policies import SoftmaxPolicy


def test_reinforce(self):

    def loss(log_probs):
        return (- log_probs.mean())
    states = State(torch.randn(3, STATE_DIM), torch.tensor([1, 1, 1]))
    actions = self.policy.eval(states).sample()
    log_probs = self.policy(states).log_prob(actions)
    tt.assert_almost_equal(log_probs, torch.tensor([(- 0.84), (- 0.62), (- 0.757)]), decimal=3)
    self.policy.reinforce(loss(log_probs))
    log_probs = self.policy(states).log_prob(actions)
    tt.assert_almost_equal(log_probs, torch.tensor([(- 0.811), (- 0.561), (- 0.701)]), decimal=3)
    self.policy.reinforce(loss(log_probs))
    log_probs = self.policy(states).log_prob(actions)
    tt.assert_almost_equal(log_probs, torch.tensor([(- 0.785), (- 0.51), (- 0.651)]), decimal=3)
