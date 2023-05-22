import torch
import torch.nn as nn
from torch.nn import functional as F
from ute.utils.arg_pars import opt
from ute.utils.logging_setup import logger


def __init__(self):
    super(MLP, self).__init__()
    self.fc1 = nn.Linear(opt.feature_dim, (opt.embed_dim * 2))
    self.fc2 = nn.Linear((opt.embed_dim * 2), opt.embed_dim)
    self.fc_last = nn.Linear(opt.embed_dim, 1)
    self._init_weights()
