import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import BertModel
from common import *


def lin_layer(n_in, n_out, dropout):
    return nn.Sequential(nn.Linear(n_in, n_out), GELU(), nn.Dropout(dropout))
