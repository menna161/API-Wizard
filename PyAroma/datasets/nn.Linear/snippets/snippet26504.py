import torch
import torch.nn as nn
from torch.autograd import Variable


def __init__(self, ninput, nhidden, nlayers, nvocab, pretrained=False, vocab=None, type_emb=False, ninput2=0, nvocab2=0, rnn_type='GRU', dropout=0.2, use_cuda=True):
    super(LSTMLM, self).__init__()
    self.dropout = nn.Dropout(dropout)
    self.embedding = nn.Embedding(nvocab, ninput)
    if type_emb:
        assert ((ninput2 > 0) and (nvocab2 > 0)), 'set the emb and vocab size for word type.'
        self.embedding2 = nn.Embedding(nvocab2, ninput2)
        ninput = (ninput + ninput2)
        print('RNN size {}'.format(ninput))
    self.rnn = nn.GRU(ninput, nhidden, nlayers, dropout=dropout, batch_first=True)
    self.linear_out = nn.Linear(nhidden, nvocab)
    self.rnn_type = rnn_type
    self.nhidden = nhidden
    self.nlayers = nlayers
    self.use_cuda = use_cuda
    self.type_emb = type_emb
    self.pretrained = pretrained
    self.vocab = vocab
    self.init_weights()
