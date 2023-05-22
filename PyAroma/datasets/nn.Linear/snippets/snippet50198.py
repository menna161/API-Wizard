from collections import defaultdict
from os.path import join, dirname, abspath
import copy
import sys
import random
import torch
import torch.nn as nn
import numpy as np
from scipy.stats import entropy, sem
from sklearn.metrics import roc_auc_score
from evidence_inference.models.utils import PaddedSequence
from evidence_inference.preprocess.preprocessor import SimpleInferenceVectorizer
import pdb


def __init__(self, encoding_size, query_dims=0, condition_attention=False, tokenwise_attention=False):
    super(TokenAttention, self).__init__()
    self.condition_attention = condition_attention
    if condition_attention:
        self.attn_MLP_hidden_dims = 32
        self.attn_input_dims = (encoding_size + query_dims)
        self.token_attention_F = nn.Sequential(nn.Linear(self.attn_input_dims, self.attn_MLP_hidden_dims), nn.Tanh(), nn.Linear(self.attn_MLP_hidden_dims, 1))
    else:
        self.token_attention_F = nn.Linear(encoding_size, 1)
    if tokenwise_attention:
        self.attn_sm = nn.Sigmoid()
    else:
        self.attn_sm = nn.Softmax(dim=1)
