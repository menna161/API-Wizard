import math
import torch


def __init__(self, input_size, hidden_size, output_size, drop_rate):
    super(PositionwiseFeedForward, self).__init__()
    self.ff1 = torch.nn.Linear(input_size, hidden_size)
    self.ff2 = torch.nn.Linear(hidden_size, output_size)
    self.drop = torch.nn.Dropout(drop_rate)
