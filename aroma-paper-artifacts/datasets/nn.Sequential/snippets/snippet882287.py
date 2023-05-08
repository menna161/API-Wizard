import torch
from torch import nn
from torch.distributions.independent import Independent
from torch.distributions.normal import Normal


def __init__(self, x_dim=1600, z_dim=2):
    net = nn.Sequential(nn.Linear(x_dim, 300), nn.ReLU(), nn.Linear(300, 300), nn.ReLU(), nn.Linear(300, z_dim))
    super(PlanarEncoder, self).__init__(net, x_dim, z_dim)
