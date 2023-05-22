import pytest
import numpy as np
import torch
import torch_testing as tt
import gym
from rlil import nn
from rlil.environments import State


def test_dueling(setUp):
    torch.random.manual_seed(0)
    value_model = nn.Linear(2, 1)
    advantage_model = nn.Linear(2, 3)
    model = nn.Dueling(value_model, advantage_model)
    states = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
    result = model(states).detach().numpy()
    np.testing.assert_array_almost_equal(result, np.array([[(- 0.495295), 0.330573, 0.678836], [(- 1.253222), 1.509323, 2.502186]], dtype=np.float32))
