import random
import numpy as np
import sys
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F
from .attention import Attention
from .baseRNN import BaseRNN
import torch.cuda as device
import torch as device


def __init__(self, vocab_size, max_len, hidden_size, sos_id, eos_id, n_layers=1, rnn_cell='gru', bidirectional=False, input_dropout_p=0, dropout_p=0, use_attention=False):
    super(DecoderRNN, self).__init__(vocab_size, max_len, hidden_size, input_dropout_p, dropout_p, n_layers, rnn_cell)
    self.bidirectional_encoder = bidirectional
    self.rnn = self.rnn_cell(hidden_size, hidden_size, n_layers, batch_first=True, dropout=dropout_p)
    self.output_size = vocab_size
    self.max_length = max_len
    self.use_attention = use_attention
    self.eos_id = eos_id
    self.sos_id = sos_id
    self.init_input = None
    self.embedding = nn.Embedding(self.output_size, self.hidden_size)
    if use_attention:
        self.attention = Attention(self.hidden_size)
    self.out = nn.Linear(self.hidden_size, self.output_size)
