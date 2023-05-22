import numpy as np
import torch
from rlil import nn


def fc_dynamics(env, hidden1=500, hidden2=500):
    return nn.Sequential(nn.Linear((env.state_space.shape[0] + env.action_space.shape[0]), hidden1), nn.LeakyReLU(), nn.Linear(hidden1, hidden2), nn.LeakyReLU(), nn.Linear(hidden2, env.state_space.shape[0]))
