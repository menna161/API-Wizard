import math
import torch
import torch.nn as nn


def __init__(self, input_size, hidden_size, n_layers=1, input_dropout_p=0, dropout_p=0, bidirectional=False, rnn_cell='gru', variable_lengths=False):
    super(EncoderRNN, self).__init__()
    self.hidden_size = hidden_size
    self.bidirectional = bidirectional
    self.n_layers = n_layers
    self.dropout_p = dropout_p
    self.variable_lengths = variable_lengths
    if (rnn_cell.lower() == 'lstm'):
        self.rnn_cell = nn.LSTM
    elif (rnn_cell.lower() == 'gru'):
        self.rnn_cell = nn.GRU
    else:
        raise ValueError('Unsupported RNN Cell: {0}'.format(rnn_cell))
    '\n        Copied from https://github.com/SeanNaren/deepspeech.pytorch/blob/master/model.py\n        Copyright (c) 2017 Sean Naren\n        MIT License\n        '
    outputs_channel = 32
    self.conv = MaskConv(nn.Sequential(nn.Conv2d(1, outputs_channel, kernel_size=(41, 11), stride=(2, 2), padding=(20, 5)), nn.BatchNorm2d(outputs_channel), nn.Hardtanh(0, 20, inplace=True), nn.Conv2d(outputs_channel, outputs_channel, kernel_size=(21, 11), stride=(2, 1), padding=(10, 5)), nn.BatchNorm2d(outputs_channel), nn.Hardtanh(0, 20, inplace=True)))
    rnn_input_dims = int(((math.floor(((input_size + (2 * 20)) - 41)) / 2) + 1))
    rnn_input_dims = int(((math.floor(((rnn_input_dims + (2 * 10)) - 21)) / 2) + 1))
    rnn_input_dims *= outputs_channel
    self.rnn = self.rnn_cell(rnn_input_dims, self.hidden_size, self.n_layers, dropout=self.dropout_p, bidirectional=self.bidirectional)
