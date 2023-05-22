import random
import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F
from .attention import Attention
import torch.cuda as device
import torch as device


def __init__(self, vocab_size, max_len, hidden_size, encoder_size, sos_id, eos_id, n_layers=1, rnn_cell='gru', bidirectional_encoder=False, bidirectional_decoder=False, dropout_p=0, use_attention=True):
    super(DecoderRNN, self).__init__()
    self.output_size = vocab_size
    self.vocab_size = vocab_size
    self.hidden_size = hidden_size
    self.bidirectional_encoder = bidirectional_encoder
    self.bidirectional_decoder = bidirectional_decoder
    self.encoder_output_size = ((encoder_size * 2) if self.bidirectional_encoder else encoder_size)
    self.n_layers = n_layers
    self.dropout_p = dropout_p
    self.max_length = max_len
    self.use_attention = use_attention
    self.eos_id = eos_id
    self.sos_id = sos_id
    if (rnn_cell.lower() == 'lstm'):
        self.rnn_cell = nn.LSTM
    elif (rnn_cell.lower() == 'gru'):
        self.rnn_cell = nn.GRU
    else:
        raise ValueError('Unsupported RNN Cell: {0}'.format(rnn_cell))
    self.init_input = None
    self.rnn = self.rnn_cell((self.hidden_size + self.encoder_output_size), self.hidden_size, self.n_layers, batch_first=True, dropout=dropout_p, bidirectional=self.bidirectional_decoder)
    self.embedding = nn.Embedding(self.vocab_size, self.hidden_size)
    self.input_dropout = nn.Dropout(self.dropout_p)
    self.attention = Attention(dec_dim=self.hidden_size, enc_dim=self.encoder_output_size, conv_dim=1, attn_dim=self.hidden_size)
    self.fc = nn.Linear((self.hidden_size + self.encoder_output_size), self.output_size)
