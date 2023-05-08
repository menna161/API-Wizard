import torch
from torch import Tensor, nn
from torch.jit import Final


def __init__(self, config):
    super().__init__()
    self.eps = config.eps
    self.register_buffer('n_fft', torch.tensor([320]))
    self.register_buffer('hop', torch.tensor([config.stft_hop]))
    self.n_freq_bins = ((self.n_fft.item() // 2) + 1)
    config.n_freq_bins = self.n_freq_bins
    self.register_buffer('hann', torch.hann_window(self.n_fft.item()))
    self.register_buffer('hann_sq', self.hann.pow(2))
    self.register_buffer('hann_norm', self.hann_sq.sum().sqrt())
    self.register_buffer('sr', torch.tensor([config.sr]))
    self.norm = ExponentialDecay(alpha=config.norm_alpha)
    self.norm_init_length = config.norm_init_length
    self.db_mult = float(config.norm_db_mult)
    in_features = (config.n_freq_bins * 2)
    self.fc_clc_1 = nn.Linear(in_features, in_features)
    self.bn_clc_1 = nn.BatchNorm1d(in_features)
    self.rnn_clc = nn.GRU(in_features, config.rnn_n_hidden_clc, config.rnn_n_layers_clc, bidirectional=False, dropout=float(config.rnn_dropout), bias=True)
    self.fc_clc_2 = nn.Linear(config.rnn_n_hidden_clc, config.rnn_n_hidden_clc)
    self.bn_clc_2 = nn.BatchNorm1d(config.rnn_n_hidden_clc)
    if (config.clc_max_freq > 0):
        self.clc_n_bins = int(floor((config.clc_max_freq / 250)))
    else:
        self.clc_n_bins = config.n_freq_bins
    self.fc_clc_out = nn.Linear(config.rnn_n_hidden_clc, ((self.clc_n_bins * config.clc_order) * 2), bias=True)
    self.out_act_f = config.out_act_factor
    self.clc_order = config.clc_order
    self.clc_offset = config.clc_offset
    self.clc_lookahead = config.clc_lookahead
    self.n_freq_bins = config.n_freq_bins
