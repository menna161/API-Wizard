from __future__ import division
from __future__ import absolute_import
import torch
from torch import nn
from torch import distributions
import torch.nn.functional as F
from .CaptioningModel import CaptioningModel


def __init__(self, vocab_size, img_feat_size, input_encoding_size, rnn_size, dropout_prob_lm, ss_prob=0.0):
    super(FC, self).__init__()
    self.vocab_size = vocab_size
    self.img_feat_size = img_feat_size
    self.input_encoding_size = input_encoding_size
    self.rnn_size = rnn_size
    self.embed = nn.Embedding(vocab_size, input_encoding_size)
    self.fc_image = nn.Linear(img_feat_size, input_encoding_size)
    self.lstm_cell = LSTMCell(input_encoding_size, rnn_size, dropout_prob_lm)
    self.out_fc = nn.Linear(rnn_size, vocab_size)
    self.ss_prob = ss_prob
    self.init_weights()
