import math
import torch


def forward(self, input_):
    ' \n        HT+X(1-T)\n        '
    hh = torch.relu(self.ff1(input_))
    tt = torch.sigmoid(self.ff2(input_))
    return self.drop(((hh * tt) + (input_ * (1 - tt))))
