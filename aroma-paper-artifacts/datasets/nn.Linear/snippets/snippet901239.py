import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from onqg.models.modules.Attention import ScaledDotProductAttention
from onqg.models.modules.MaxOut import MaxOut


def __init__(self, state_dim, dropout=0.1):
    super(Propagator, self).__init__()
    self.reset_gate = nn.Sequential(nn.Linear((state_dim * 3), state_dim), nn.Sigmoid(), nn.Dropout(dropout))
    self.update_gate = nn.Sequential(nn.Linear((state_dim * 3), state_dim), nn.Sigmoid(), nn.Dropout(dropout))
    self.transform = nn.Sequential(nn.Linear((state_dim * 3), state_dim), nn.Tanh())
