import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import copy
from transformers.modeling_gpt2 import *


def __init__(self, config):
    super(GPT2MemLMHeadModel, self).__init__(config)
    self.transformer = GPT2MemModel(config)
    self.init_weights()
    self.tie_weights()
