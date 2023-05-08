import torch
from torch import nn
from torch.distributions.independent import Independent
from torch.distributions.normal import Normal


def __init__(self, armotized, z_dim=2, u_dim=2):
    net_hidden = nn.Sequential(nn.Linear((z_dim + u_dim), 20), nn.ReLU(), nn.Linear(20, 20), nn.ReLU())
    net_mean = nn.Linear(20, z_dim)
    net_logstd = nn.Linear(20, z_dim)
    if armotized:
        net_A = nn.Linear(20, (z_dim ** 2))
        net_B = nn.Linear(20, (u_dim * z_dim))
    else:
        (net_A, net_B) = (None, None)
    super(PlanarDynamics, self).__init__(net_hidden, net_mean, net_logstd, net_A, net_B, z_dim, u_dim, armotized)
