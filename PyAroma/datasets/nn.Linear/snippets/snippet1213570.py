import torch
from torch import nn, optim
from torchtext import data
from catalyst.dl import SupervisedRunner
from catalyst.dl.callbacks import AccuracyCallback
from torch.utils.data import DataLoader
from torchtext.data import Iterator
from gensim.models import KeyedVectors


def __init__(self, num_embeddings, embedding_dim=300, hidden_size=300, output_size=1, num_layers=1, dropout=0.2):
    super().__init__()
    model = KeyedVectors.load_word2vec_format('ch07/GoogleNews-vectors-negative300.bin', binary=True)
    weights = torch.FloatTensor(model.vectors)
    self.emb = nn.Embedding.from_pretrained(weights)
    self.lstm = nn.LSTM(embedding_dim, hidden_size, num_layers, batch_first=True, dropout=dropout, bidirectional=True)
    self.linear = nn.Linear((hidden_size * 2), output_size)
