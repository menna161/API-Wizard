import math
import torch


def __init__(self, hidden_size, drop_rate):
    super(HighwayFeedForward, self).__init__()
    self.ff1 = torch.nn.Linear(hidden_size, hidden_size)
    self.ff2 = torch.nn.Linear(hidden_size, hidden_size)
    self.drop = torch.nn.Dropout(drop_rate)
