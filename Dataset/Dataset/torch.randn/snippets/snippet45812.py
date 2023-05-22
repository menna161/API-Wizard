import math
import torch


def __init__(self, input_size, fm_size):
    super(CompressionFM, self).__init__()
    self.LW = torch.nn.Linear(input_size, 1)
    self.QV = torch.nn.Parameter(torch.randn(input_size, fm_size))
