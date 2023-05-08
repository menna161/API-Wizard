import numpy as np
import torch
from sklearn.datasets import make_blobs


def __init__(self, input_size, hidden_size):
    super(Feedforward, self).__init__()
    self.input_size = input_size
    self.hidden_size = hidden_size
    self.fc1 = torch.nn.Linear(self.input_size, self.hidden_size)
    self.act1 = torch.nn.Tanh()
