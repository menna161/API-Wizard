import numpy as np
import torch
from rlil import nn


def fc_actor_critic(env, hidden1=400, hidden2=300):
    features = nn.Sequential(nn.Linear(env.state_space.shape[0], hidden1), nn.LeakyReLU())
    v = nn.Sequential(nn.Linear(hidden1, hidden2), nn.LeakyReLU(), nn.Linear(hidden2, 1))
    policy = nn.Sequential(nn.Linear(hidden1, hidden2), nn.LeakyReLU(), nn.Linear(hidden2, (env.action_space.shape[0] * 2)))
    return (features, v, policy)
