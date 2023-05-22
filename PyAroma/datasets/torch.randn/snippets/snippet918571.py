import torch
import torch.nn as nn
from utils import to_var
import torch.nn.functional as torch_f


def __init__(self, config):
    super(ConvScoreSSREM, self).__init__()
    self.config = config
    self.mat_M = nn.Parameter(torch.randn([config.embedding_size, config.embedding_size], dtype=torch.float32), requires_grad=True)
    self.logsoftmax = nn.LogSoftmax(dim=1)
    self.score_active_func = nn.Tanh()
