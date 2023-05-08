import math
import torch
import torch.nn.functional as F


def __init__(self, n_heads, hidden_size, drop_rate):
    super().__init__()
    assert ((hidden_size % n_heads) == 0)
    self.n_dk = (hidden_size // n_heads)
    self.n_heads = n_heads
    self.proj_query = torch.nn.Linear(hidden_size, hidden_size)
    self.proj_key = torch.nn.Linear(hidden_size, hidden_size)
    self.proj_value = torch.nn.Linear(hidden_size, hidden_size)
    self.dropout = torch.nn.Dropout(drop_rate)
    self.proj_output = torch.nn.Linear(hidden_size, hidden_size)
