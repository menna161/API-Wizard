import torch
from torch import nn
from torch.distributions.independent import Independent
from torch.distributions.normal import Normal


def __init__(self, armotized, z_dim=8, u_dim=3):
    net_hidden = nn.Sequential(nn.Linear((z_dim + u_dim), 40), nn.ReLU(), nn.Linear(40, 40), nn.ReLU())
    net_mean = nn.Linear(40, z_dim)
    net_logstd = nn.Linear(40, z_dim)
    if armotized:
        net_A = nn.Linear(40, (z_dim * z_dim))
        net_B = nn.Linear(40, (u_dim * z_dim))
    else:
        (net_A, net_B) = (None, None)
    super(ThreePoleDynamics, self).__init__(net_hidden, net_mean, net_logstd, net_A, net_B, z_dim, u_dim, armotized)
