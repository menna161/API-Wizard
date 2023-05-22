import torch.nn as nn


def __init__(self, rnn_type, ntoken, ninp, nhid, nlayers, dropout=0.5, tie_weights=False):
    super(RNNModel, self).__init__()
    self.drop = nn.Dropout(dropout)
    self.encoder = nn.Embedding(ntoken, ninp)
    if (rnn_type in ['LSTM', 'GRU']):
        self.rnn = getattr(nn, rnn_type)(ninp, nhid, nlayers, dropout=dropout)
    else:
        try:
            nonlinearity = {'RNN_TANH': 'tanh', 'RNN_RELU': 'relu'}[rnn_type]
        except KeyError:
            raise ValueError("An invalid option for `--model` was supplied,\n                                 options are ['LSTM', 'GRU', 'RNN_TANH' or 'RNN_RELU']")
        self.rnn = nn.RNN(ninp, nhid, nlayers, nonlinearity=nonlinearity, dropout=dropout)
    self.decoder = nn.Linear(nhid, ntoken)
    if tie_weights:
        if (nhid != ninp):
            raise ValueError('When using the tied flag, nhid must be equal to emsize')
        self.decoder.weight = self.encoder.weight
    self.init_weights()
    self.rnn_type = rnn_type
    self.nhid = nhid
    self.nlayers = nlayers
