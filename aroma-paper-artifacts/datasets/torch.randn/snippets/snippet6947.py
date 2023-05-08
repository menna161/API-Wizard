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


def test_step_one(self):
    state = State(torch.randn(1, STATE_DIM))
    vae_action = Action(torch.randn(1, ACTION_DIM))
    self.policy(state, vae_action)
    self.policy.step()