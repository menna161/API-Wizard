import torch
import torch.nn as nn
import numpy as np
import math


def __init__(self, dim, attn_dim=64, dropout=0.1):
    super(GatedSelfAttention, self).__init__()
    self.m_translate = nn.Linear(dim, attn_dim)
    self.q_translate = nn.Linear(dim, attn_dim)
    self.update = nn.Linear((2 * dim), dim, bias=False)
    self.gate = nn.Linear((2 * dim), dim, bias=False)
    if (dropout > 0):
        self.dropout = nn.Dropout(dropout)
    self.has_dropout = (True if (dropout > 0) else False)
