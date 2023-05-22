import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, vocab_size: int, embed_dim: int, hidden_dim: int, embed_drop: float):
    super().__init__()
    self.embedding = nn.Embedding(vocab_size, embed_dim)
    self.conv = nn.Conv1d(in_channels=embed_dim, out_channels=hidden_dim, kernel_size=3, padding=1)
    self.embed_dropout = nn.Dropout(embed_drop)
    self.linear = nn.Linear(hidden_dim, embed_dim)
