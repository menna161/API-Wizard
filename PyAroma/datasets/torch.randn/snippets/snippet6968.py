import unittest
import torch
from torch import nn
import torch_testing as tt
from rlil.environments import State
from rlil.policies import SoftmaxPolicy


def test_multi_action(self):
    states = State(torch.randn(3, STATE_DIM))
    actions = self.policy(states).sample()
    tt.assert_equal(actions, torch.tensor([2, 2, 0]))
