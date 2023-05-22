import pytest
import numpy as np
import torch
from torch import nn
import torch_testing as tt
from gym.spaces import Box
from rlil.environments import State
from rlil.policies import SoftDeterministicPolicy


def test_reinforce_one(setUp):
    policy = setUp
    state = State(torch.randn(1, STATE_DIM))
    (action, log_prob1) = policy(state)
    loss = (- log_prob1.mean())
    policy.reinforce(loss)
    (action, log_prob2) = policy(state)
    assert (log_prob2.item() > log_prob1.item())
