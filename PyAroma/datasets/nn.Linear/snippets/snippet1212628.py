import torch.nn as nn


def __init__(self, d_model, d_ff, dropout=0.1):
    super(PositionwiseFeedForward, self).__init__()
    self.w_1 = nn.Linear(d_model, d_ff)
    self.w_2 = nn.Linear(d_ff, d_model)
    self.layer_norm = nn.LayerNorm(d_model, eps=1e-06)
    self.dropout_1 = nn.Dropout(dropout)
    self.relu = nn.ReLU()
    self.dropout_2 = nn.Dropout(dropout)
