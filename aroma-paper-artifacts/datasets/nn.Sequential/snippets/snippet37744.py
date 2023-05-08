import torch
import torch.nn as nn


def __init__(self, config):
    super(SNLIClassifier, self).__init__()
    self.config = config
    self.embed = nn.Embedding(config.n_embed, config.d_embed)
    self.projection = Linear(config.d_embed, config.d_proj)
    self.encoder = Encoder(config)
    self.dropout = nn.Dropout(p=config.dp_ratio)
    self.relu = nn.ReLU()
    seq_in_size = (2 * config.d_hidden)
    if self.config.birnn:
        seq_in_size *= 2
    lin_config = ([seq_in_size] * 2)
    self.out = nn.Sequential(Linear(*lin_config), self.relu, self.dropout, Linear(*lin_config), self.relu, self.dropout, Linear(*lin_config), self.relu, self.dropout, Linear(seq_in_size, config.d_out))
