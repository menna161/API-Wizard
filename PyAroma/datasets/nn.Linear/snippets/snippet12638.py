import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


def __init__(self, in_dim, out_dim, bias=True, w_init_gain='linear'):
    super(LinearNorm, self).__init__()
    self.linear_layer = torch.nn.Linear(in_dim, out_dim, bias=bias)
    torch.nn.init.xavier_uniform_(self.linear_layer.weight, gain=torch.nn.init.calculate_gain(w_init_gain))
