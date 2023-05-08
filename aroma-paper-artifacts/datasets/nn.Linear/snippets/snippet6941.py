import pytest
import numpy as np
import torch
import torch_testing as tt
import gym
from rlil import nn
from rlil.environments import State


def test_perturb_noisy_layers(setUp):
    inputs = torch.tensor([[3.0, (- 2.0), 10]])
    model1 = nn.Sequential(nn.Linear(3, 3), nn.NoisyFactorizedLinear(3, 3))
    help_perturb_noisy_layers(model1, inputs)
    model2 = nn.Sequential(nn.Linear(3, 3), nn.NoisyLinear(3, 3))
    help_perturb_noisy_layers(model2, inputs)
    model3 = nn.RLNetwork(nn.Sequential(nn.Linear(3, 3), nn.NoisyLinear(3, 3)))
    help_perturb_noisy_layers(model3, State(inputs))
