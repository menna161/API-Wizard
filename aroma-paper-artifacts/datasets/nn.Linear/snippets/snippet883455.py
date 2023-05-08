import math
import os
from collections import OrderedDict
from dataclasses import field, dataclass
from torch import nn
from typing import Dict, List, Union, Callable
from models import Seq2Seq
from sonosco.models.modules import MaskConv, BatchRNN, SequenceWise, InferenceBatchSoftmax
from sonosco.model.serializer import Serializer
from sonosco.model.deserializer import Deserializer
from sonosco.model.serialization import serializable
from abc import ABC, abstractmethod


def __post_init__(self):
    super(MockModel, self).__init__()
    sample_rate = self.audio_conf.get('sample_rate', 16000)
    window_size = self.audio_conf.get('window_size', 0.02)
    num_classes = len(self.labels)
    self.conv = MaskConv(nn.Sequential(nn.Conv2d(1, 32, kernel_size=(41, 11), stride=(2, 2), padding=(20, 5)), nn.BatchNorm2d(32), nn.Hardtanh(0, 20, inplace=True), nn.Conv2d(32, 32, kernel_size=(21, 11), stride=(2, 1), padding=(10, 5)), nn.BatchNorm2d(32), nn.Hardtanh(0, 20, inplace=True)))
    rnn_in_size = int((math.floor(((sample_rate * window_size) / 2)) + 1))
    rnn_in_size = int(((math.floor(((rnn_in_size + (2 * 20)) - 41)) / 2) + 1))
    rnn_in_size = int(((math.floor(((rnn_in_size + (2 * 10)) - 21)) / 2) + 1))
    rnn_in_size *= 32
    rnns = [('0', BatchRNN(input_size=rnn_in_size, hidden_size=self.rnn_hid_size, rnn_type=self.rnn_type, batch_norm=False))]
    rnns.extend([(f'{(x + 1)}', BatchRNN(input_size=self.rnn_hid_size, hidden_size=self.rnn_hid_size, rnn_type=self.rnn_type)) for x in range((self.nb_layers - 1))])
    self.rnns = nn.Sequential(OrderedDict(rnns))
    fully_connected = nn.Sequential(nn.BatchNorm1d(self.rnn_hid_size), nn.Linear(self.rnn_hid_size, num_classes, bias=False))
    self.fc = nn.Sequential(SequenceWise(fully_connected))
    self.inference_softmax = InferenceBatchSoftmax()
