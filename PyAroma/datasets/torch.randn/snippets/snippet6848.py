import unittest
import torch
import gym
from torch import nn
from torch.nn.functional import smooth_l1_loss
import torch_testing as tt
import numpy as np
from rlil.environments import State, Action
from rlil.approximation import QNetwork, FixedTarget


def test_eval_actions(self):
    states = State(torch.randn(3, STATE_DIM))
    Action.set_action_space(action_space)
    actions = Action(torch.tensor([1, 2, 0]).unsqueeze(1))
    result = self.q.eval(states, actions)
    self.assertEqual(result.shape, torch.Size([3]))
    tt.assert_almost_equal(result, torch.tensor([(- 0.7262873), 0.3484948, (- 0.0296164)]))
