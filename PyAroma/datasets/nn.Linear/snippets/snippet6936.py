import pytest
import numpy as np
import torch
import torch_testing as tt
import gym
from rlil import nn
from rlil.environments import State


def test_categorical_dueling(setUp):
    n_actions = 2
    n_atoms = 3
    value_model = nn.Linear(2, n_atoms)
    advantage_model = nn.Linear(2, (n_actions * n_atoms))
    model = nn.CategoricalDueling(value_model, advantage_model)
    x = torch.randn((2, 2))
    out = model(x)
    assert (out.shape == (2, 6))
    tt.assert_almost_equal(out, torch.tensor([[0.014, (- 0.691), 0.251, (- 0.055), (- 0.419), (- 0.03)], [0.057, (- 1.172), 0.568, (- 0.868), (- 0.482), (- 0.679)]]), decimal=3)
