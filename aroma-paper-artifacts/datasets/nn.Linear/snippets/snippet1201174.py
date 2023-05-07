import torch
from torch import nn
from torch.nn import Parameter
import torch.nn.functional as F
from utils import gelu, LayerNorm, get_incremental_state, set_incremental_state
import math


def __init__(self, embed_dim, num_heads, dropout=0.0, weights_dropout=True):
    super(MultiheadAttention, self).__init__()
    self.embed_dim = embed_dim
    self.num_heads = num_heads
    self.dropout = dropout
    self.head_dim = (embed_dim // num_heads)
    assert ((self.head_dim * num_heads) == self.embed_dim), 'embed_dim must be divisible by num_heads'
    self.scaling = (self.head_dim ** (- 0.5))
    self.in_proj_weight = Parameter(torch.Tensor((3 * embed_dim), embed_dim))
    self.in_proj_bias = Parameter(torch.Tensor((3 * embed_dim)))
    self.out_proj = nn.Linear(embed_dim, embed_dim, bias=True)
    self.weights_dropout = weights_dropout
    self.reset_parameters()
