import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Dict
from dataclasses import field
from collections import OrderedDict
from sonosco.serialization import serializable
from sonosco.blocks.modules import SubsampleBlock, TDSBlock, Linear
from sonosco.blocks.attention import DotProductAttention


def __post_init__(self):
    super(Decoder, self).__init__()
    self.encoder_hidden_size = self.hidden_size
    self.embedding = nn.Embedding(self.vocab_size, self.embedding_dim)
    self.rnn = nn.ModuleList()
    self.rnn += [nn.LSTMCell((self.embedding_dim + self.encoder_hidden_size), self.hidden_size)]
    for l in range(1, self.num_layers):
        self.rnn += [nn.LSTMCell(self.hidden_size, self.hidden_size)]
    self.attention = DotProductAttention()
    self.mlp = nn.Sequential(nn.Linear((self.encoder_hidden_size + self.hidden_size), self.hidden_size), nn.Tanh(), nn.Linear(self.hidden_size, self.vocab_size))
