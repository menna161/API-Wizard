import unittest
import torch
from torch import nn
import torch_testing as tt
from rlil.environments import State
from rlil.policies import SoftmaxPolicy


def test_run(self):
    state1 = State(torch.randn(1, STATE_DIM))
    dist1 = self.policy(state1)
    action1 = dist1.sample()
    log_prob1 = dist1.log_prob(action1)
    self.assertEqual(action1.item(), 0)
    state2 = State(torch.randn(1, STATE_DIM))
    dist2 = self.policy(state2)
    action2 = dist2.sample()
    log_prob2 = dist2.log_prob(action2)
    self.assertEqual(action2.item(), 2)
    loss = (- (torch.tensor([(- 1), 1000000]) * torch.cat((log_prob1, log_prob2))).mean())
    self.policy.reinforce(loss)
    state3 = State(torch.randn(1, STATE_DIM))
    dist3 = self.policy(state3)
    action3 = dist3.sample()
    self.assertEqual(action3.item(), 2)
