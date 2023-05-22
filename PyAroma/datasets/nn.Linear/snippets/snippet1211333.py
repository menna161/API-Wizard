import copy
import math
import datetime
import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, d_model, nhead, dim_feedforward=2048, dropout=0.1, activation='relu', attn=False, conv=False, convsz=1, shared_qk=False, sep=False):
    super(ConformerEncoderLayer, self).__init__()
    self.conv = conv
    if conv:
        assert ((convsz % 2) == 1)
        self.conv_layer = nn.Conv1d(d_model, d_model, convsz, padding=int(((convsz - 1) / 2)), groups=nhead)
    self.attn = attn
    if attn:
        self.self_attn = MultiheadSeparableAttention(d_model, nhead, dropout=dropout, shared_qk=shared_qk, sep=sep)
    self.linear1 = nn.Linear(d_model, dim_feedforward)
    self.dropout = nn.Dropout(dropout)
    self.linear2 = nn.Linear(dim_feedforward, d_model)
    self.norm1 = nn.LayerNorm(d_model)
    self.norm2 = nn.LayerNorm(d_model)
    self.dropout1 = nn.Dropout(dropout)
    self.dropout2 = nn.Dropout(dropout)
    self.activation = _get_activation_fn(activation)
