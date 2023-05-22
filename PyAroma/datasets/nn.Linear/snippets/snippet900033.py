import torch
import torch.nn as nn
import random


def __init__(self, input_size, hidden_size, n_layer=1, bidirectional=False):
    super(DecoderRNN, self).__init__()
    self.input_size = input_size
    self.hidden_size = hidden_size
    self.bidirectional = bidirectional
    self.num_directions = (2 if bidirectional else 1)
    self.n_units_hidden1 = 256
    self.n_units_hidden2 = 128
    self.gru = nn.GRU(input_size, hidden_size, n_layer, bidirectional=bidirectional, dropout=(0.2 if (n_layer == 2) else 0))
    self.linear1 = nn.Sequential(nn.Linear(hidden_size, self.n_units_hidden1), nn.LeakyReLU(True), nn.Linear(self.n_units_hidden1, (input_size - 6)))
    self.linear2 = nn.Sequential(nn.Linear(hidden_size, self.n_units_hidden2), nn.ReLU(True), nn.Dropout(0.2), nn.Linear(self.n_units_hidden2, 6))
    self.linear3 = nn.Sequential(nn.Linear(hidden_size, self.n_units_hidden2), nn.ReLU(True), nn.Dropout(0.2), nn.Linear(self.n_units_hidden2, 1))
    self.lockdrop = LockedDropout()
    self.dropout_i = 0.2
    self.dropout_o = 0.2
    self.init_input = self.initInput()
