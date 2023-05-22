import torch
import torch.nn as nn
import torch.nn.functional as F
import math


def __init__(self, dim_X, dim_Y, dim, num_heads=4, ln=False, p=None):
    super().__init__()
    self.num_heads = num_heads
    self.fc_q = nn.Linear(dim_X, dim)
    self.fc_k = nn.Linear(dim_Y, dim)
    self.fc_v = nn.Linear(dim_Y, dim)
    self.fc_o = nn.Linear(dim, dim)
    self.ln1 = (nn.LayerNorm(dim) if ln else nn.Identity())
    self.ln2 = (nn.LayerNorm(dim) if ln else nn.Identity())
    self.dropout1 = (nn.Dropout(p=p) if (p is not None) else nn.Identity())
    self.dropout2 = (nn.Dropout(p=p) if (p is not None) else nn.Identity())
