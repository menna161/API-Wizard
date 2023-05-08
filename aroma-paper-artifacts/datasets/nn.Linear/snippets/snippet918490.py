import random
import torch
from torch import nn
from torch.nn import functional as F
from .rnncells import StackedGRUCell, LSTMSACell
from .beam_search import Beam
from utils import to_var, SOS_ID, UNK_ID, EOS_ID


def __init__(self, vocab_size, embedding_size, hidden_size, rnncell=StackedGRUCell, num_layers=1, dropout=0.0, word_drop=0.0, max_unroll=30, sample=True, temperature=1.0, beam_size=1):
    super(DecoderRNN, self).__init__()
    self.vocab_size = vocab_size
    self.embedding_size = embedding_size
    self.hidden_size = hidden_size
    self.num_layers = num_layers
    self.dropout = dropout
    self.temperature = temperature
    self.word_drop = word_drop
    self.max_unroll = max_unroll
    self.sample = sample
    self.beam_size = beam_size
    self.embedding = nn.Embedding(vocab_size, embedding_size)
    self.rnncell = rnncell(num_layers, embedding_size, hidden_size, dropout)
    self.out = nn.Linear(hidden_size, vocab_size)
    self.softmax = nn.Softmax(dim=1)
