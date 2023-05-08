import torch
import torch.nn as nn
import torch.nn.functional as F
from utils.display import *
from utils.dsp import *


def __init__(self, hidden_size=896, quantisation=256):
    super(WaveRNN, self).__init__()
    self.hidden_size = hidden_size
    self.split_size = (hidden_size // 2)
    self.R = nn.Linear(self.hidden_size, (3 * self.hidden_size), bias=False)
    self.O1 = nn.Linear(self.split_size, self.split_size)
    self.O2 = nn.Linear(self.split_size, quantisation)
    self.O3 = nn.Linear(self.split_size, self.split_size)
    self.O4 = nn.Linear(self.split_size, quantisation)
    self.I_coarse = nn.Linear(2, (3 * self.split_size), bias=False)
    self.I_fine = nn.Linear(3, (3 * self.split_size), bias=False)
    self.bias_u = nn.Parameter(torch.zeros(self.hidden_size))
    self.bias_r = nn.Parameter(torch.zeros(self.hidden_size))
    self.bias_e = nn.Parameter(torch.zeros(self.hidden_size))
    self.num_params()
