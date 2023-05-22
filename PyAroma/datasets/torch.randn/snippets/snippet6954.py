import pytest
import unittest
import torch
import torch_testing as tt
import numpy as np
from gym.spaces import Box
from rlil import nn
from rlil.approximation import FixedTarget
from rlil.environments import State
from rlil.policies import DeterministicPolicy


def test_converge(self):
    state = State(torch.randn(1, STATE_DIM))
    target = torch.tensor([0.25, 0.5, (- 0.5)])
    for _ in range(0, 200):
        action = self.policy(state)
        loss = ((target - action) ** 2).mean()
        self.policy.reinforce(loss)
    self.assertLess(loss, 0.001)
