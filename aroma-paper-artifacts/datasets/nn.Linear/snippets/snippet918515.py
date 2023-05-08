import torch
import torch.nn as nn


def __init__(self, input_size, hidden_size):
    super(LSTMSACell, self).__init__()
    self.input_size = input_size
    self.hidden_size = hidden_size
    self.u12u = nn.Linear(input_size, input_size, bias=False)
    self.u22u = nn.Linear(input_size, input_size, bias=False)
    self.x2h = nn.Linear(input_size, (4 * hidden_size), bias=True)
    self.u2h = nn.Linear(input_size, (4 * hidden_size), bias=True)
    self.h2h = nn.Linear(hidden_size, (4 * hidden_size), bias=True)
