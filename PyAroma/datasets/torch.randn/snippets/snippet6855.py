import unittest
import torch
from torch import nn
import torch_testing as tt
from rlil.approximation.v_network import VNetwork
from rlil.environments import State


def test_reinforce_list(self):
    states = State(torch.randn(5, STATE_DIM), mask=torch.tensor([1, 1, 0, 1, 0]))
    result = self.v(states)
    tt.assert_almost_equal(result, torch.tensor([0.7053187, 0.3975691, 0.0, 0.2701665, 0.0]))
    self.v.reinforce(loss(result, torch.tensor([1, (- 1), 1, 1, 1])).float())
    result = self.v(states)
    tt.assert_almost_equal(result, torch.tensor([0.9732854, 0.5453826, 0.0, 0.4344811, 0.0]))
