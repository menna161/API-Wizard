import torch
from torch import nn
import torch.nn.functional as F


def __init__(self, dim, heads=8, causal=False, compression_factor=3, dropout=0.0):
    super().__init__()
    assert ((dim % heads) == 0), 'dimension must be divisible by number of heads'
    self.heads = heads
    self.causal = causal
    self.compression_factor = compression_factor
    self.compress_fn = ConvCompress(dim, compression_factor, groups=heads)
    self.to_qkv = nn.Linear(dim, (dim * 3), bias=False)
    self.to_out = nn.Linear(dim, dim)
    self.dropout = nn.Dropout(dropout)
    self.null_k = nn.Parameter(torch.zeros(1, 1, dim))
    self.null_v = nn.Parameter(torch.zeros(1, 1, dim))
