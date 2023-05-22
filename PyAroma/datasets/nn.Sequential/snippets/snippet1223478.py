import torch
import torch.nn as nn
from torch.distributions import MultivariateNormal
import numpy as np
from tqdm import tqdm
import copy
import os


def __init__(self, in_dim, out_dim, hidden_dim):
    super().__init__()
    self.net = nn.Sequential(nn.Linear(in_dim, hidden_dim), nn.Tanh(), nn.Linear(hidden_dim, hidden_dim), nn.Tanh(), nn.Linear(hidden_dim, out_dim))
