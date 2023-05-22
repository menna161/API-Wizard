import matplotlib.pylab as plt
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


def __init__(self, env, n_layers=1, hidden_dim=8, activation=nn.ReLU):
    super(NNPolicy, self).__init__(env)
    layers = []
    in_dim = self.obs_dim
    for _ in range(n_layers):
        layers.append(nn.BatchNorm1d(in_dim, affine=False))
        layers.append(nn.Linear(in_dim, hidden_dim))
        layers.append(activation())
        in_dim = hidden_dim
    layers.append(nn.Linear(in_dim, self.ac_dim))
    self.seq = nn.Sequential(*layers)
    self.epsilon = 1.0
