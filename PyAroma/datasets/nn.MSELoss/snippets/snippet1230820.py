import torch
from torch import nn, Tensor
from typing import Union, Tuple, List, Iterable, Dict


def forward(self, sentence_features: Iterable[Dict[(str, Tensor)]], labels: Tensor):
    rep = self.model(sentence_features[0])['sentence_embedding']
    loss_fct = nn.MSELoss()
    loss = loss_fct(rep, labels)
    return loss
