import os
import copy
import warnings
import numpy as np
import pickle
from tqdm import tqdm
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parameter import Parameter
from torch.utils.data import DataLoader
from torch.optim import Optimizer
from torch_geometric.nn import GATConv
from torch_sparse import SparseTensor
from ...dataloader.graph_data import Graph_Processer
from ..basic_model import Basic_Model
from ...sampler import Basic_Sampler
from ...utils import *
import warnings


def __init__(self, in_dim: int, out_dim: int, z_dims: list, hid_dims: list, num_heads: int, device='gpu'):
    "\n        Inputs:\n            in_dims     : [int] Length of the vocabulary for convolutional layers in WHAI;\n            z_dims      : [list] Number of topics at different layers in WHAI;\n            h_dims      : [list] Size of dimension at different hidden layers in WHAI;\n            device      : [str] 'cpu' or 'gpu';\n\n        Attributes:\n            h_encoder       : [Modulelist] the graph nerual network layers for latent representation for WGAAE\n            shaep_encoder   : [Modulelist] the linear layers for shape-parameters in Weibull distribution\n            scale_encoder   : [Modulelist] the linear layers for scale-parameters in Weibull distribution\n\n            fc_layers       : [Modulelist] the linear layers for WGAAE_encoder\n            skip_layers     : [Modulelist] the skip layers for WGAAE_encoder\n            norm_layers     : [Modulelist] the batch normalization layers for WGAAE_encoder\n        "
    super(WGAAE_Encoder, self).__init__()
    self.in_dim = in_dim
    self.out_dim = out_dim
    self.z_dims = z_dims
    self.hid_dims = hid_dims
    self.num_layers = len(hid_dims)
    self.num_heads = num_heads
    self.device = device
    self.real_min = torch.tensor(2.2e-10, dtype=torch.float, device=self.device)
    self.theta_max = torch.tensor(1000.0, dtype=torch.float, device=self.device)
    self.wei_shape_min = torch.tensor(0.1, dtype=torch.float, device=self.device)
    self.wei_shape_max = torch.tensor(1000.0, dtype=torch.float, device=self.device)
    self.fc_layers = nn.ModuleList()
    self.skip_layers = nn.ModuleList()
    self.norm_layers = nn.ModuleList()
    self.h_encoders = nn.ModuleList()
    self.shape_encoders = nn.ModuleList()
    self.scale_encoders = nn.ModuleList()
    self.in_hid_dims = ([self.in_dim] + self.hid_dims)
    for layer in range(self.num_layers):
        self.h_encoders.append(GATConv(self.in_hid_dims[layer], (self.in_hid_dims[(layer + 1)] // self.num_heads), heads=self.num_heads, dropout=0.6).to(self.device))
        self.shape_encoders.append(nn.Linear(self.z_dims[layer], self.z_dims[layer]).to(self.device))
        self.scale_encoders.append(nn.Linear(self.z_dims[layer], self.z_dims[layer]).to(self.device))
        self.skip_layers.append(nn.Linear(self.in_hid_dims[layer], self.in_hid_dims[(layer + 1)]).to(self.device))
        self.norm_layers.append(nn.BatchNorm1d(self.in_hid_dims[(layer + 1)]).to(self.device))
        self.fc_layers.append(nn.Linear(self.in_hid_dims[(layer + 1)], self.z_dims[layer]).to(self.device))
