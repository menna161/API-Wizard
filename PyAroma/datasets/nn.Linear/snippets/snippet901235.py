import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from onqg.models.modules.Attention import ScaledDotProductAttention
from onqg.models.modules.MaxOut import MaxOut


def __init__(self, n_head, d_model, d_k, d_v, addition_input=0, dropout=0.1, attn_dropout=0.1):
    super().__init__()
    self.n_head = n_head
    self.d_k = d_k
    self.d_v = d_v
    self.w_qs = nn.Linear(d_model, (n_head * d_k))
    self.w_ks = nn.Linear((d_model + addition_input), (n_head * d_k))
    self.w_vs = nn.Linear((d_model + addition_input), (n_head * d_v))
    nn.init.normal_(self.w_qs.weight, mean=0, std=np.sqrt((2.0 / (d_model + d_k))))
    nn.init.normal_(self.w_ks.weight, mean=0, std=np.sqrt((2.0 / ((d_model + addition_input) + d_k))))
    nn.init.normal_(self.w_vs.weight, mean=0, std=np.sqrt((2.0 / ((d_model + addition_input) + d_v))))
    self.attention = ScaledDotProductAttention(temperature=np.power(d_k, 0.5), attn_dropout=attn_dropout)
    self.layer_norm = nn.LayerNorm(d_model)
    self.fc = nn.Linear((n_head * d_v), d_model)
    nn.init.xavier_normal_(self.fc.weight)
    self.dropout = nn.Dropout(dropout)
