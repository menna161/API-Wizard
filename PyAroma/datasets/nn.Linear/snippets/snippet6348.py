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
    super(BLSTMprojEncoder, self).__init__()
    self.bsize = config['bsize']
    self.word_emb_dim = config['word_emb_dim']
    self.enc_lstm_dim = config['enc_lstm_dim']
    self.pool_type = config['pool_type']
    self.dpout_model = config['dpout_model']
    self.enc_lstm = nn.LSTM(self.word_emb_dim, self.enc_lstm_dim, 1, bidirectional=True, dropout=self.dpout_model)
    self.init_lstm = Variable(torch.FloatTensor(2, self.bsize, self.enc_lstm_dim).zero_()).cuda()
    self.proj_enc = nn.Linear((2 * self.enc_lstm_dim), (2 * self.enc_lstm_dim), bias=False)
