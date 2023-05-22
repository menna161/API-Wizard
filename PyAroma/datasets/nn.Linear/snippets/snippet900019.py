import torch.nn as nn
import torch


def __init__(self, h_dim, z_dim):
    super(Discriminator, self).__init__()
    main = nn.Sequential(nn.Linear(z_dim, h_dim), nn.LeakyReLU(inplace=True), nn.Linear(h_dim, h_dim), nn.LeakyReLU(inplace=True), nn.Linear(h_dim, h_dim), nn.LeakyReLU(inplace=True), nn.Linear(h_dim, 1))
    self.main = main
    self.apply(weights_init)
