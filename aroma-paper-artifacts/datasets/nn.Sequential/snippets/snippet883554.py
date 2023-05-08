import math
import torch
import logging
import torch.nn as nn
from collections import OrderedDict
from sonosco.blocks.modules import MaskConv, BatchRNN, SequenceWise, InferenceBatchSoftmax, supported_rnns, supported_rnns_inv


def __init__(self, rnn_type=nn.LSTM, labels='abc', rnn_hidden_size=768, hidden_layers=5, audio_conf=None, bidirectional=True):
    super(DeepSpeech2, self).__init__()
    if (audio_conf is None):
        audio_conf = {}
    self.version = '0.0.1'
    self.hidden_size = rnn_hidden_size
    self.hidden_layers = hidden_layers
    self.rnn_type = rnn_type
    self.audio_conf = (audio_conf or {})
    self.labels = labels
    self.bidirectional = bidirectional
    sample_rate = self.audio_conf.get('sample_rate', 16000)
    window_size = self.audio_conf.get('window_size', 0.02)
    num_classes = len(self.labels)
    self.conv = MaskConv(nn.Sequential(nn.Conv2d(1, 32, kernel_size=(41, 11), stride=(2, 2), padding=(20, 5)), nn.BatchNorm2d(32), nn.Hardtanh(0, 20, inplace=True), nn.Conv2d(32, 32, kernel_size=(21, 11), stride=(2, 1), padding=(10, 5)), nn.BatchNorm2d(32), nn.Hardtanh(0, 20, inplace=True)))
    rnn_in_size = int((math.floor(((sample_rate * window_size) / 2)) + 1))
    LOGGER.debug(f'Initial calculated feature size: {rnn_in_size}')
    rnn_in_size = int(((math.floor(((rnn_in_size + (2 * 20)) - 41)) / 2) + 1))
    rnn_in_size = int(((math.floor(((rnn_in_size + (2 * 10)) - 21)) / 2) + 1))
    rnn_in_size *= 32
    rnns = [('0', BatchRNN(input_size=rnn_in_size, hidden_size=rnn_hidden_size, rnn_type=rnn_type, batch_norm=False, bidirectional=bidirectional))]
    rnns.extend([(f'{(x + 1)}', BatchRNN(input_size=rnn_hidden_size, hidden_size=rnn_hidden_size, rnn_type=rnn_type, bidirectional=bidirectional)) for x in range((hidden_layers - 1))])
    self.rnns = nn.Sequential(OrderedDict(rnns))
    fully_connected = nn.Sequential(nn.BatchNorm1d(rnn_hidden_size), nn.Linear(rnn_hidden_size, num_classes, bias=False))
    self.fc = nn.Sequential(SequenceWise(fully_connected))
    self.inference_softmax = InferenceBatchSoftmax()
