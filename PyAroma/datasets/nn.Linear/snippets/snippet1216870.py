import torch
from torch import nn
import torch.nn.functional as F
from mogrifier import Mogrifier
import math
from collections import namedtuple
from functools import partial
from inspect import isfunction


def __init__(self, dim, seq_len, mem_len, cmem_len, cmem_ratio=4, heads=8, attn_dropout=0.0, dropout=0.0, reconstruction_attn_dropout=0.0):
    super().__init__()
    assert ((dim % heads) == 0), 'dimension must be divisible by the number of heads'
    self.heads = heads
    self.dim_head = (dim // heads)
    self.seq_len = seq_len
    self.mem_len = mem_len
    self.cmem_len = cmem_len
    self.cmem_ratio = cmem_ratio
    self.scale = (self.dim_head ** (- 0.5))
    self.compress_mem_fn = ConvCompress(dim, cmem_ratio)
    self.to_q = nn.Linear(dim, dim, bias=False)
    self.to_kv = nn.Linear(dim, (dim * 2), bias=False)
    self.to_out = nn.Linear(dim, dim)
    self.attn_dropout = nn.Dropout(attn_dropout)
    self.dropout = nn.Dropout(dropout)
    self.reconstruction_attn_dropout = nn.Dropout(reconstruction_attn_dropout)
