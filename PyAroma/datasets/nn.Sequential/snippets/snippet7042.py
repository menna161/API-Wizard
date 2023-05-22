import numpy as np
import torch
from rlil import nn


def fc_bcq_decoder(env, latent_dim=32, hidden1=300, hidden2=400):
    return nn.Sequential(nn.Linear((env.state_space.shape[0] + latent_dim), hidden1), nn.LeakyReLU(), nn.Linear(hidden1, hidden2), nn.LeakyReLU(), nn.Linear(hidden2, env.action_space.shape[0]))
