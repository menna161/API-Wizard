import torch.nn as nn
from .baseRNN import BaseRNN


def __init__(self, feature_size, hidden_size, input_dropout_p=0, dropout_p=0, n_layers=1, bidirectional=False, rnn_cell='gru', variable_lengths=False, encoder_conv='base'):
    super(EncoderRNN, self).__init__(0, 0, hidden_size, input_dropout_p, dropout_p, n_layers, rnn_cell)
    self.variable_lengths = variable_lengths
    self.conv = nn.Sequential(nn.Conv2d(1, 16, kernel_size=3, padding=1, bias=False), nn.BatchNorm2d(16), nn.Hardtanh(0, 20, inplace=True), nn.Conv2d(16, 32, kernel_size=3, padding=1, bias=False), nn.BatchNorm2d(32), nn.Hardtanh(0, 20, inplace=True), nn.Conv2d(32, 64, kernel_size=3, padding=1, bias=False), nn.BatchNorm2d(64), nn.Hardtanh(0, 20, inplace=True), nn.MaxPool2d(2, 2), nn.Conv2d(64, 128, kernel_size=3, padding=1, bias=False), nn.BatchNorm2d(128), nn.Hardtanh(0, 20, inplace=True), nn.MaxPool2d(2, 2), nn.Conv2d(128, 256, kernel_size=3, padding=1, bias=False), nn.BatchNorm2d(256), nn.Hardtanh(0, 20, inplace=True))
    feature_size *= 64
    self.rnn = self.rnn_cell(feature_size, hidden_size, n_layers, batch_first=True, bidirectional=bidirectional, dropout=dropout_p)
