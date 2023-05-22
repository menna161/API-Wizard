import torch
import torch.nn as nn
from models.tae import get_sinusoid_encoding_table
import copy


def __init__(self, input_size, nker, seq_len, nfc, positions=None):
    super(TempConv, self).__init__()
    self.input_size = input_size
    self.seq_len = seq_len
    self.name = 'TempCNN_'
    self.nker = copy.deepcopy(nker)
    self.nfc = copy.deepcopy(nfc)
    self.name += '|'.join(list(map(str, self.nker)))
    if (self.nfc is not None):
        self.name += 'FC'
        self.name += '|'.join(list(map(str, self.nfc)))
    conv_layers = []
    self.nker.insert(0, input_size)
    for i in range((len(self.nker) - 1)):
        conv_layers.extend([nn.Conv1d(self.nker[i], self.nker[(i + 1)], kernel_size=3, padding=1), nn.BatchNorm1d(self.nker[(i + 1)]), nn.ReLU()])
    self.conv1d = nn.Sequential(*conv_layers)
    self.nfc.insert(0, (self.nker[(- 1)] * seq_len))
    lin_layers = []
    for i in range((len(self.nfc) - 1)):
        lin_layers.extend([nn.Linear(self.nfc[i], self.nfc[(i + 1)]), nn.BatchNorm1d(self.nfc[(i + 1)]), nn.ReLU()])
    self.linear = nn.Sequential(*lin_layers)
    if (positions is not None):
        self.position_enc = nn.Embedding.from_pretrained(get_sinusoid_encoding_table(positions, input_size, T=1000), freeze=True)
    else:
        self.position_enc = None
