import torch
from torch import nn
from torch.distributions.independent import Independent
from torch.distributions.normal import Normal


def __init__(self, x_dim=(2, 80, 80), z_dim=8):
    x_channels = x_dim[0]
    net = nn.Sequential(nn.Conv2d(in_channels=x_channels, out_channels=32, kernel_size=5, stride=1, padding=2), nn.ReLU(), nn.Conv2d(in_channels=32, out_channels=32, kernel_size=5, stride=2, padding=2), nn.ReLU(), nn.Conv2d(in_channels=32, out_channels=32, kernel_size=5, stride=2, padding=2), nn.ReLU(), nn.Conv2d(in_channels=32, out_channels=10, kernel_size=5, stride=2, padding=2), nn.ReLU(), Flatten(), nn.Linear(((10 * 10) * 10), 200), nn.ReLU(), nn.Linear(200, z_dim))
    super(CartPoleEncoder, self).__init__(net, x_dim, z_dim)
