import torch
from torch import nn
import torch.nn.functional as F
from mogrifier import Mogrifier
import math
from collections import namedtuple
from functools import partial
from inspect import isfunction


def __init__(self, num_tokens, dim, seq_len, depth, emb_dim=None, memory_layers=None, enhanced_recurrence=True, mem_len=None, cmem_len=None, cmem_ratio=4, heads=8, gru_gated_residual=True, mogrify_gru=False, attn_dropout=0.0, ff_glu=False, ff_dropout=0.0, attn_layer_dropout=0.0, reconstruction_attn_dropout=0.0, reconstruction_loss_weight=1.0):
    super().__init__()
    emb_dim = default(emb_dim, dim)
    mem_len = default(mem_len, seq_len)
    cmem_len = default(cmem_len, (mem_len // cmem_ratio))
    memory_layers = default(memory_layers, list(range(1, (depth + 1))))
    assert (mem_len >= seq_len), 'length of memory should be at least the sequence length'
    assert (cmem_len >= (mem_len // cmem_ratio)), f'length of compressed memory should be at least the memory length divided by the compression ratio {int((mem_len // cmem_ratio))}'
    assert all([((layer > 0) and (layer <= depth)) for layer in memory_layers]), 'one of the indicated memory layers is invalid'
    self.seq_len = seq_len
    self.depth = depth
    self.memory_layers = list(memory_layers)
    self.enhanced_recurrence = enhanced_recurrence
    self.token_emb = nn.Embedding(num_tokens, emb_dim)
    self.to_model_dim = (nn.Identity() if (emb_dim == dim) else nn.Linear(emb_dim, dim))
    seq_and_mem_len = ((seq_len + mem_len) + cmem_len)
    self.pos_emb = nn.Parameter(torch.zeros(heads, seq_and_mem_len, (dim // heads)))
    self.to_logits = nn.Sequential((nn.Identity() if (emb_dim == dim) else nn.Linear(dim, emb_dim)), nn.Linear(emb_dim, num_tokens))
    wrapper = (partial(GRUGating, dim, mogrify=mogrify_gru) if gru_gated_residual else Residual)
    self.attn_layers = nn.ModuleList([wrapper(PreNorm(dim, SelfAttention(dim, seq_len, mem_len, cmem_len, cmem_ratio, heads, dropout=attn_layer_dropout, attn_dropout=attn_dropout, reconstruction_attn_dropout=reconstruction_attn_dropout))) for _ in range(depth)])
    self.ff_layers = nn.ModuleList([wrapper(PreNorm(dim, FeedForward(dim, dropout=ff_dropout, glu=ff_glu))) for _ in range(depth)])
    self.reconstruction_loss_weight = reconstruction_loss_weight
