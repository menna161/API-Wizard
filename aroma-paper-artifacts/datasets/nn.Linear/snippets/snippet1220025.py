from __future__ import division
from __future__ import absolute_import
import torch
from torch import nn
from torch import distributions
import torch.nn.functional as F
from .CaptioningModel import CaptioningModel


def __init__(self, input_encoding_size, rnn_size, dropout_prob_lm):
    super(LSTMCell, self).__init__()
    self.input_encoding_size = input_encoding_size
    self.hidden_size = rnn_size
    self.dropout_prob = dropout_prob_lm
    self.i2h = nn.Linear(self.input_encoding_size, (5 * self.hidden_size))
    self.h2h = nn.Linear(self.hidden_size, (5 * self.hidden_size))
    self.dropout = nn.Dropout(p=self.dropout_prob)
    self.init_weights()
