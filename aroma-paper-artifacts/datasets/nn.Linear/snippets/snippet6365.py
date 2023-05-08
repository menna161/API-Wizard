import numpy as np
import time
import torch
from torch.autograd import Variable
import torch.nn as nn
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import warnings
import warnings


def __init__(self, config):
    super(ClassificationNet, self).__init__()
    self.nonlinear_fc = config['nonlinear_fc']
    self.fc_dim = config['fc_dim']
    self.n_classes = config['n_classes']
    self.enc_lstm_dim = config['enc_lstm_dim']
    self.encoder_type = config['encoder_type']
    self.dpout_fc = config['dpout_fc']
    self.encoder = eval(self.encoder_type)(config)
    self.inputdim = (2 * self.enc_lstm_dim)
    self.inputdim = ((4 * self.inputdim) if (self.encoder_type == 'ConvNetEncoder') else self.inputdim)
    self.inputdim = (self.enc_lstm_dim if (self.encoder_type == 'LSTMEncoder') else self.inputdim)
    self.classifier = nn.Sequential(nn.Linear(self.inputdim, 512), nn.Linear(512, self.n_classes))
