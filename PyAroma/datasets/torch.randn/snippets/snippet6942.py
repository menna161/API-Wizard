import pytest
import numpy as np
import torch
import torch_testing as tt
import gym
from rlil import nn
from rlil.environments import State


def test_mmd(setUp):
    batch_size = 10
    sample_size = 5
    dimension = 3
    sample_actions1 = torch.randn([batch_size, sample_size, dimension])
    sample_actions2 = torch.randn([batch_size, sample_size, dimension])
    nn.mmd_laplacian(sample_actions1, sample_actions2)
    nn.mmd_gaussian(sample_actions1, sample_actions2)
