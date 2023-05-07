import torch
import torch.nn as nn
import random


def forward(self, input, hidden):
    '\n\n        :param input: (1, batch, output_size)\n        :param hidden: initial hidden state\n        :return:\n            output: (1, batch, num_directions * hidden_size)\n            hidden: (num_layers * 1, batch, hidden_size)\n            output_seq: (batch, 1 * output_size)\n            stop_sign: (batch, 1)\n        '
    input = self.lockdrop(input, self.dropout_i)
    (output, hidden) = self.gru(input, hidden)
    (hidden1, hidden2) = torch.split(hidden, 1, 0)
    output_code = self.linear1(hidden1.squeeze(0))
    output_param = self.linear2(hidden2.squeeze(0))
    stop_sign = self.linear3(hidden1.squeeze(0))
    output_seq = torch.cat([output_code, output_param], dim=1)
    return (output, hidden, output_seq, stop_sign)
