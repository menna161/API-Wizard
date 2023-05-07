import math
import warnings
import torch
import torch.nn as nn
from onmt.modules.util_class import Elementwise


def __init__(self, vec_size, emb_dim, position_encoding=False, dropout=0):
    super(VecEmbedding, self).__init__()
    self.embedding_size = emb_dim
    self.proj = nn.Linear(vec_size, emb_dim, bias=False)
    self.word_padding_idx = 0
    self.position_encoding = position_encoding
    if self.position_encoding:
        self.pe = PositionalEncoding(dropout, self.embedding_size)
