import torch
from torch import nn
from torch.distributions.independent import Independent
from torch.distributions.normal import Normal


def __init__(self, x_dim=4608, z_dim=3):
    net = nn.Sequential(nn.Linear(x_dim, 500), nn.ReLU(), nn.Linear(500, 500), nn.ReLU(), nn.Linear(500, z_dim))
    super(PendulumEncoder, self).__init__(net, x_dim, z_dim)
