import torch.nn as nn
import torch


def __init__(self, n_dim, h_dim, z_dim):
    super(Generator, self).__init__()
    main = nn.Sequential(nn.Linear(n_dim, h_dim), nn.LeakyReLU(inplace=True), nn.Linear(h_dim, h_dim), nn.LeakyReLU(inplace=True), nn.Linear(h_dim, h_dim), nn.LeakyReLU(inplace=True), nn.Linear(h_dim, z_dim))
    self.main = main
    self.apply(weights_init)
