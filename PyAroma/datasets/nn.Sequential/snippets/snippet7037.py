import numpy as np
import torch
from rlil import nn


def fc_deterministic_noisy_policy(env, hidden1=400, hidden2=300):
    return nn.Sequential(nn.NoisyFactorizedLinear(env.state_space.shape[0], hidden1), nn.LeakyReLU(), nn.NoisyFactorizedLinear(hidden1, hidden2), nn.LeakyReLU(), nn.NoisyFactorizedLinear(hidden2, env.action_space.shape[0]))
