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


def test_step_one(self):
    state = State(torch.randn(1, STATE_DIM))
    self.policy(state)
    self.policy.step()
