import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from tqdm import tqdm
import copy
import os


def __init__(self, in_dim, hid_dims, z_dim, device: str='cpu'):
    super(VAE_Decoder, self).__init__()
    self.in_dim = in_dim
    self.hid_dims = hid_dims
    self.z_dim = z_dim
    self.num_layers = len(self.hid_dims)
    self.device = device
    self.fc_decoder = nn.ModuleList()
    for layer_index in range(self.num_layers):
        if (layer_index == 0):
            self.fc_decoder.append(nn.Linear(self.z_dim, self.hid_dims[layer_index]).to(device))
        else:
            self.fc_decoder.append(nn.Linear(self.hid_dims[(layer_index - 1)], self.hid_dims[layer_index]).to(device))
    self.fc_decoder.append(nn.Linear(self.hid_dims[(- 1)], self.in_dim).to(device))
