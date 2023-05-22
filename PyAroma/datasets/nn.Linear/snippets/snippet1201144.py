import torch
from torch import nn
from torch.nn import Parameter
import torch.nn.functional as F
from utils import gelu, LayerNorm, get_incremental_state, set_incremental_state
import math


def __init__(self, embed_dim, ff_embed_dim, num_heads, dropout, with_external=False, weights_dropout=True):
    super(TransformerLayer, self).__init__()
    self.self_attn = MultiheadAttention(embed_dim, num_heads, dropout, weights_dropout)
    self.fc1 = nn.Linear(embed_dim, ff_embed_dim)
    self.fc2 = nn.Linear(ff_embed_dim, embed_dim)
    self.attn_layer_norm = LayerNorm(embed_dim)
    self.ff_layer_norm = LayerNorm(embed_dim)
    self.with_external = with_external
    self.dropout = dropout
    if self.with_external:
        self.external_attn = MultiheadAttention(embed_dim, num_heads, dropout, weights_dropout)
        self.external_layer_norm = LayerNorm(embed_dim)
    self.reset_parameters()
