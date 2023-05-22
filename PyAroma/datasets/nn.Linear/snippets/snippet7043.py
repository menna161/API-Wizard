import numpy as np
import torch
from rlil import nn


def fc_bcq_deterministic_policy(env, hidden1=400, hidden2=300):
    return nn.Sequential(nn.Linear((env.state_space.shape[0] + env.action_space.shape[0]), hidden1), nn.LeakyReLU(), nn.Linear(hidden1, hidden2), nn.LeakyReLU(), nn.Linear(hidden2, env.action_space.shape[0]))
