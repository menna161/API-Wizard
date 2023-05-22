import torch.nn as nn
import torch.nn.functional as F
from torch.nn.utils.rnn import pack_padded_sequence as pack
from torch.nn.utils.rnn import pad_packed_sequence as unpack
from onmt.encoders.encoder import EncoderBase
from onmt.utils.rnn_factory import rnn_factory


def _initialize_bridge(self, rnn_type, hidden_size, num_layers):
    number_of_states = (2 if (rnn_type == 'LSTM') else 1)
    self.total_hidden_dim = (hidden_size * num_layers)
    self.bridge = nn.ModuleList([nn.Linear(self.total_hidden_dim, self.total_hidden_dim, bias=True) for _ in range(number_of_states)])
