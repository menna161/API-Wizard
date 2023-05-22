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
    super(ConvNetEncoder, self).__init__()
    self.bsize = config['bsize']
    self.word_emb_dim = config['word_emb_dim']
    self.enc_lstm_dim = config['enc_lstm_dim']
    self.pool_type = config['pool_type']
    self.convnet1 = nn.Sequential(nn.Conv1d(self.word_emb_dim, (2 * self.enc_lstm_dim), kernel_size=3, stride=1, padding=1), nn.ReLU(inplace=True))
    self.convnet2 = nn.Sequential(nn.Conv1d((2 * self.enc_lstm_dim), (2 * self.enc_lstm_dim), kernel_size=3, stride=1, padding=1), nn.ReLU(inplace=True))
    self.convnet3 = nn.Sequential(nn.Conv1d((2 * self.enc_lstm_dim), (2 * self.enc_lstm_dim), kernel_size=3, stride=1, padding=1), nn.ReLU(inplace=True))
    self.convnet4 = nn.Sequential(nn.Conv1d((2 * self.enc_lstm_dim), (2 * self.enc_lstm_dim), kernel_size=3, stride=1, padding=1), nn.ReLU(inplace=True))
