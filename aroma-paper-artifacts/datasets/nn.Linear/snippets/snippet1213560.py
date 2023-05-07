import torch
from torch import nn, optim
from torchtext import data
from catalyst.dl import SupervisedRunner
from catalyst.dl.callbacks import AccuracyCallback
from torch.utils.data import DataLoader
from torchtext.data import Iterator


def __init__(self, num_embeddings, embedding_dim=50, hidden_size=50, output_size=1, num_layers=1, dropout=0.2):
    super().__init__()
    self.emb = nn.Embedding(num_embeddings, embedding_dim, padding_idx=0)
    self.lstm = nn.LSTM(embedding_dim, hidden_size, num_layers, batch_first=True, dropout=dropout)
    self.linear = nn.Linear(hidden_size, output_size)
