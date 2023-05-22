import torch
from torch import nn
from torch.nn import functional as F
import numpy as np
from lib.utils.vis_logger import logger
from math import pi, sqrt, log
from math import pi, sqrt, log


def __init__(self, dim_in, dim_conv, dim_hidden, dim_out, n_layers, kernel_size, stride):
    '\n        :param dim_in: input channels\n        :param dim_conv: conv output channels\n        :param dim_hidden: MLP and LSTM output dim\n        :param dim_out: latent variable dimension\n        '
    nn.Module.__init__(self)
    self.mlc = MultiLayerConv(dim_in, dim_conv, n_layers, kernel_size, stride=stride)
    self.mlp = MLP(dim_conv, dim_hidden, n_layers=1)
    self.lstm = nn.LSTMCell((dim_hidden + (4 * dim_out)), dim_hidden)
    self.mean_update = nn.Linear(dim_hidden, dim_out)
    self.logvar_update = nn.Linear(dim_hidden, dim_out)
