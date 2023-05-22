import pytest
import numpy as np
import torch
import torch_testing as tt
import gym
from rlil import nn
from rlil.environments import State


def test_list(setUp):
    model = nn.Linear(2, 2)
    net = nn.RLNetwork(model, (2,))
    features = torch.randn((4, 2))
    done = torch.tensor([1, 1, 0, 1], dtype=torch.bool)
    out = net(State(features, done))
    tt.assert_almost_equal(out, torch.tensor([[0.0479387, (- 0.2268031)], [0.2346841, 0.0743403], [0.0, 0.0], [0.2204496, 0.086818]]))
    features = torch.randn(3, 2)
    done = torch.tensor([1, 1, 1], dtype=torch.bool)
    out = net(State(features, done))
    tt.assert_almost_equal(out, torch.tensor([[0.4234636, 0.1039939], [0.6514298, 0.3354351], [(- 0.2543002), (- 0.2041451)]]))
