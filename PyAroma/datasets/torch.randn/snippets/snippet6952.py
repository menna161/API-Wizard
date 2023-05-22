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


def test_output_shape(self):
    state = State(torch.randn(1, STATE_DIM))
    action = self.policy(state)
    self.assertEqual(action.shape, (1, ACTION_DIM))
    state = State(torch.randn(5, STATE_DIM))
    action = self.policy(state)
    self.assertEqual(action.shape, (5, ACTION_DIM))
