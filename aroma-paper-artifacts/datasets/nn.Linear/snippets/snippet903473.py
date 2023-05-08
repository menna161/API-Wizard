import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import copy
from transformers.modeling_gpt2 import *


def __init__(self, config):
    super(GPT2NeighborLMHeadModel, self).__init__(config)
    self.transformer = GPT2NeighborModel(config)
    self.lm_head = nn.Linear(config.n_embd, config.vocab_size, bias=False)
    self.init_weights()
    self.tie_weights()
