import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, vocab_size: int, embed_dim: int, hidden_dim: int, n_layer: int, embed_drop: float, rnn_drop: float):
    super().__init__()
    self.embedding = nn.Embedding(vocab_size, embed_dim)
    self.bilstm = nn.LSTM(embed_dim, (hidden_dim // 2), num_layers=n_layer, dropout=(rnn_drop if (n_layer > 1) else 0), batch_first=True, bidirectional=True)
    self.embed_dropout = nn.Dropout(embed_drop)
    self.linear = nn.Linear(hidden_dim, embed_dim)
