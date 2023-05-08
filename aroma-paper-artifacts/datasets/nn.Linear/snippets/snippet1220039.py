import torch
import torch.nn as nn
import torch.nn.init
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
from torch.nn.utils.weight_norm import weight_norm
from torch.nn.utils.clip_grad import clip_grad_norm
import numpy as np
from collections import OrderedDict
from .VisualSemanticModel import VisualSemanticModel


def __init__(self, img_dim, embed_size, no_imgnorm=False):
    super(EncoderImagePrecomp, self).__init__()
    self.embed_size = embed_size
    self.no_imgnorm = no_imgnorm
    self.fc = nn.Linear(img_dim, embed_size)
    self.init_weights()
