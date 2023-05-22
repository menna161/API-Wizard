import copy
import math
import datetime
import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, embed_dim, num_heads, dropout=0.0, bias=True, add_bias_kv=False, add_zero_attn=False, kdim=None, vdim=None, shared_qk=False, sep=False):
    super(MultiheadSeparableAttention, self).__init__()
    self.embed_dim = embed_dim
    self.kdim = (kdim if (kdim is not None) else embed_dim)
    self.vdim = (vdim if (vdim is not None) else embed_dim)
    self._qkv_same_embed_dim = ((self.kdim == embed_dim) and (self.vdim == embed_dim))
    self.num_heads = num_heads
    self.dropout = dropout
    self.head_dim = (embed_dim // num_heads)
    assert ((self.head_dim * num_heads) == self.embed_dim), 'embed_dim must be divisible by num_heads'
    self.shared_qk = shared_qk
    self.sep = sep
    if (self._qkv_same_embed_dim is False):
        self.q_proj_weight = nn.Parameter(torch.Tensor(embed_dim, embed_dim))
        self.k_proj_weight = nn.Parameter(torch.Tensor(embed_dim, self.kdim))
        self.v_proj_weight = nn.Parameter(torch.Tensor(embed_dim, self.vdim))
        self.register_parameter('in_proj_weight', None)
    else:
        if shared_qk:
            self.in_proj_weight = nn.Parameter(torch.empty((2 * embed_dim), embed_dim))
        else:
            self.in_proj_weight = nn.Parameter(torch.empty((3 * embed_dim), embed_dim))
        self.register_parameter('q_proj_weight', None)
        self.register_parameter('k_proj_weight', None)
        self.register_parameter('v_proj_weight', None)
    if bias:
        if shared_qk:
            self.in_proj_bias = nn.Parameter(torch.empty((2 * embed_dim)))
        else:
            self.in_proj_bias = nn.Parameter(torch.empty((3 * embed_dim)))
    else:
        self.register_parameter('in_proj_bias', None)
    self.out_proj = nn.Linear(embed_dim, embed_dim, bias=bias)
    if add_bias_kv:
        self.bias_k = nn.Parameter(torch.empty(1, 1, embed_dim))
        self.bias_v = nn.Parameter(torch.empty(1, 1, embed_dim))
    else:
        self.bias_k = self.bias_v = None
    self.add_zero_attn = add_zero_attn
    self._reset_parameters()
