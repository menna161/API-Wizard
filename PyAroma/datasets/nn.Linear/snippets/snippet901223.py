import torch
import torch.nn as nn


def __init__(self, d_enc, d_dec, n_enc_layer):
    self.d_enc_model = d_enc
    self.n_enc_layer = n_enc_layer
    self.d_dec_model = d_dec
    super(DecInit, self).__init__()
    self.initer = nn.Linear((self.d_enc_model * self.n_enc_layer), self.d_dec_model)
    self.tanh = nn.Tanh()
