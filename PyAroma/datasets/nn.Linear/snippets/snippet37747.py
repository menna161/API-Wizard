import torch
import torch.nn as nn


def __init__(self):
    super(Sequence, self).__init__()
    self.lstm1 = nn.LSTMCell(1, 51)
    self.lstm2 = nn.LSTMCell(51, 51)
    self.linear = nn.Linear(51, 1)
