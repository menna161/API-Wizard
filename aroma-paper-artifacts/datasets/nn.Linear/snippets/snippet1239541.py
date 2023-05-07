import torch
from torch import nn
import torchvision


def __init__(self, encoder_dim, decoder_dim, attention_dim):
    "\n        :param encoder_dim: feature size of encoded images\n        :param decoder_dim: size of decoder's RNN\n        :param attention_dim: size of the attention network\n        "
    super(Attention, self).__init__()
    self.encoder_att = nn.Linear(encoder_dim, attention_dim)
    self.decoder_att = nn.Linear(decoder_dim, attention_dim)
    self.full_att = nn.Linear(attention_dim, 1)
    self.relu = nn.ReLU()
    self.softmax = nn.Softmax(dim=1)
