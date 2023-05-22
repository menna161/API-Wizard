import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from tqdm import tqdm
import copy
import os


def __init__(self, in_dim: int, hid_dims: list, z_dim: int, device: str='cpu'):
    super(VAE_Encoder, self).__init__()
    self.in_dim = in_dim
    self.hid_dims = hid_dims
    self.z_dim = z_dim
    self.device = device
    self.num_layers = len(self.hid_dims)
    self.fc_encoder = nn.ModuleList()
    self.fc_mu = nn.Linear(self.hid_dims[(- 1)], self.z_dim).to(self.device)
    self.fc_var = nn.Linear(self.hid_dims[(- 1)], self.z_dim).to(self.device)
    for layer_index in range(self.num_layers):
        if (layer_index == 0):
            self.fc_encoder.append(nn.Linear(self.in_dim, self.hid_dims[layer_index]).to(device))
        else:
            self.fc_encoder.append(nn.Linear(self.hid_dims[(layer_index - 1)], self.hid_dims[layer_index]).to(device))
