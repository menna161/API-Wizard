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


@pytest.mark.skip
def test_converge(self):
    state = State(torch.randn(1, STATE_DIM))
    vae_action = Action(torch.randn(1, ACTION_DIM))
    target = (vae_action.features + torch.tensor([[0.25, 0.5, (- 0.5)]]))
    for _ in range(0, 200):
        action = self.policy(state, vae_action)
        loss = ((target - action) ** 2).mean()
        loss.backward()
        self.policy.step()
    self.assertLess(loss, 0.001)
