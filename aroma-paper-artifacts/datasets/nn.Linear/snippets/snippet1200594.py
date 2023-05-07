import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, dec_dim, enc_dim, conv_dim, attn_dim, smoothing=False):
    super(Attention, self).__init__()
    self.dec_dim = dec_dim
    self.enc_dim = enc_dim
    self.conv_dim = conv_dim
    self.attn_dim = attn_dim
    self.smoothing = smoothing
    self.conv = nn.Conv1d(in_channels=1, out_channels=self.attn_dim, kernel_size=3, padding=1)
    self.W = nn.Linear(self.dec_dim, self.attn_dim, bias=False)
    self.V = nn.Linear(self.enc_dim, self.attn_dim, bias=False)
    self.fc = nn.Linear(attn_dim, 1, bias=True)
    self.b = nn.Parameter(torch.rand(attn_dim))
    self.tanh = nn.Tanh()
    self.softmax = nn.Softmax(dim=(- 1))
    self.mask = None
