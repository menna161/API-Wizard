import pytest
import numpy as np
import torch
from torch import nn
import torch_testing as tt
from gym.spaces import Box
from rlil.environments import State
from rlil.policies import SoftDeterministicPolicy


def test_sample_multiple(setUp):
    policy = setUp
    state = State(torch.randn(5, STATE_DIM))
    (actions, raw_actions) = policy.sample_multiple(state, num_sample=10)
    assert (actions.shape == (5, 10, ACTION_DIM))
    assert (raw_actions.shape == (5, 10, ACTION_DIM))
