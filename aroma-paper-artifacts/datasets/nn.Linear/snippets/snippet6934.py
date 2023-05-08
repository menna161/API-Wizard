import pytest
import numpy as np
import torch
import torch_testing as tt
import gym
from rlil import nn
from rlil.environments import State


def test_linear0(setUp):
    model = nn.Linear0(3, 3)
    result = model(torch.tensor([[3.0, (- 2.0), 10]]))
    tt.assert_equal(result, torch.tensor([[0.0, 0.0, 0.0]]))
