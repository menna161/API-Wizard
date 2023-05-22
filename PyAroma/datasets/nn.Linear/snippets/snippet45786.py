import torch
from torch.autograd import Variable


def __init__(self, input_size, hidden_size, device=torch.device('cpu')):
    '\n        implementation of self-attention.\n        '
    super().__init__()
    self.ff1 = torch.nn.Linear(input_size, hidden_size)
    self.ff2 = torch.nn.Linear(hidden_size, 1, bias=False)
