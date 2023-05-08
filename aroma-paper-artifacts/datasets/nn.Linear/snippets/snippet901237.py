import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from onqg.models.modules.Attention import ScaledDotProductAttention
from onqg.models.modules.MaxOut import MaxOut


def __init__(self, d_in, d_hid, dropout=0.1):
    super().__init__()
    self.onelayer = (d_hid == d_in)
    if self.onelayer:
        self.w = nn.Linear(d_in, d_in, bias=False)
        self.tanh = nn.Tanh()
    else:
        self.w_1 = nn.Conv1d(d_in, d_hid, 1)
        self.w_2 = nn.Conv1d(d_hid, d_in, 1)
    self.layer_norm = nn.LayerNorm(d_in)
    self.dropout = nn.Dropout(dropout)
