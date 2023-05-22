import torch
import numpy as np
import torch.nn as nn
from torch.nn.utils.weight_norm import weight_norm


def __init__(self, in_dim, hid_dim, out_dim, dropout):
    super(SimpleClassifier, self).__init__()
    layers = [weight_norm(nn.Linear(in_dim, hid_dim), dim=None), nn.ReLU(), nn.Dropout(dropout, inplace=True), weight_norm(nn.Linear(hid_dim, out_dim), dim=None)]
    self.main = nn.Sequential(*layers)