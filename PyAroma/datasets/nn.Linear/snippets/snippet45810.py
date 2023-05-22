import torch
from torch.autograd import Variable


def __init__(self, src_hidden_size, trg_hidden_size, rnn_network, device=torch.device('cpu')):
    '\n        encoder rnn 2 decoder rnn.\n        '
    super(natsEncoder2Decoder, self).__init__()
    self.rnn_network = rnn_network
    self.encoder2decoder = torch.nn.Linear((2 * src_hidden_size), trg_hidden_size)
    if (rnn_network == 'lstm'):
        self.encoder2decoder_c = torch.nn.Linear((2 * src_hidden_size), trg_hidden_size)
