import pytest
import numpy as np
import torch
from torch import nn
import torch_testing as tt
from gym.spaces import Box
from rlil.environments import State
from rlil.policies import SoftDeterministicPolicy


def test_output_shape(setUp):
    policy = setUp
    state = State(torch.randn(1, STATE_DIM))
    (action, _) = policy(state)
    assert (action.shape == (1, ACTION_DIM))
    state = State(torch.randn(5, STATE_DIM))
    (action, _) = policy(state)
    assert (action.shape == (5, ACTION_DIM))
