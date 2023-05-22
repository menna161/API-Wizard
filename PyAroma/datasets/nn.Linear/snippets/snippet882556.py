import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


def __init__(self, word_size, word_dim, hidden_dim):
    super(LM, self).__init__()
    self.word_size = word_size
    self.word_dim = word_dim
    self.hidden_dim = hidden_dim
    self.word_embs = nn.Embedding(num_embeddings=word_size, embedding_dim=word_dim)
    self.fw_encoder = nn.LSTMCell(word_dim, hidden_dim)
    self.bw_encoder = nn.LSTMCell(word_dim, hidden_dim)
    self.classifier = nn.Linear((hidden_dim * 2), word_size)
    self.dropout = nn.Dropout(0.1)
