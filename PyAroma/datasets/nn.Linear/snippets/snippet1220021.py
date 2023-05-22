from __future__ import division
from __future__ import absolute_import
import torch
from torch import nn
from torch import distributions
import torch.nn.functional as F
from .CaptioningModel import CaptioningModel


def __init__(self, vocab_size, bos_idx, with_relu=False, with_visual_sentinel=False, det_feat_size=2048, input_encoding_size=1000, rnn_size=1000, att_size=512, ss_prob=0.0):
    super(BottomupTopdownAttention, self).__init__()
    self.vocab_size = vocab_size
    self.bos_idx = bos_idx
    self.with_relu = with_relu
    self.with_visual_sentinel = with_visual_sentinel
    self.det_feat_size = det_feat_size
    self.input_encoding_size = input_encoding_size
    self.rnn_size = rnn_size
    self.att_size = att_size
    self.embed = nn.Embedding(vocab_size, input_encoding_size)
    self.lstm_cell_1 = nn.LSTMCell(((det_feat_size + rnn_size) + input_encoding_size), rnn_size)
    self.lstm_cell_2 = nn.LSTMCell((rnn_size + det_feat_size), rnn_size)
    self.att_va = nn.Linear(det_feat_size, att_size, bias=False)
    self.att_ha = nn.Linear(rnn_size, att_size, bias=False)
    self.att_a = nn.Linear(att_size, 1, bias=False)
    if self.with_visual_sentinel:
        self.W_sx = nn.Linear(((det_feat_size + rnn_size) + input_encoding_size), rnn_size)
        self.W_sh = nn.Linear(rnn_size, rnn_size)
        self.W_sah = nn.Linear(rnn_size, att_size, bias=False)
        self.W_sas = nn.Linear(rnn_size, att_size, bias=False)
        self.W_sa = nn.Linear(att_size, 1, bias=False)
        self.fc_sentinel = nn.Linear(rnn_size, det_feat_size)
    self.out_fc = nn.Linear(rnn_size, vocab_size)
    self.ss_prob = ss_prob
    self.init_weights()
