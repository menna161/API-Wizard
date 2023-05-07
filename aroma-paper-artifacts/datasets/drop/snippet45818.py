import math
import torch


def forward(self, input_):
    ' \n        (B, S, D) -> (B, S, D_ff) -> (B, S, D)\n        '
    return self.drop(self.ff2(gelu(self.ff1(input_))))
