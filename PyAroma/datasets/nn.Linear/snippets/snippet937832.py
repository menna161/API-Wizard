import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, vocab_size: int, max_seq_len: int, embed_dim: int, hidden_dim: int, n_layer: int, n_head: int, ff_dim: int, embed_drop: float, hidden_drop: float):
    super().__init__()
    self.tok_embedding = nn.Embedding(vocab_size, embed_dim)
    self.pos_embedding = nn.Embedding(max_seq_len, embed_dim)
    layer = nn.TransformerEncoderLayer(d_model=hidden_dim, nhead=n_head, dim_feedforward=ff_dim, dropout=hidden_drop)
    self.encoder = nn.TransformerEncoder(layer, num_layers=n_layer)
    self.embed_dropout = nn.Dropout(embed_drop)
    self.linear1 = nn.Linear(embed_dim, hidden_dim)
    self.linear2 = nn.Linear(hidden_dim, embed_dim)
