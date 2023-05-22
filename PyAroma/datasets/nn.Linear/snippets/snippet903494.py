import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import copy
from transformers.modeling_gpt2 import *


def __init__(self, cfg, n_ctx):
    super(GatedMemoryUpdate, self).__init__()
    self.W1 = torch.nn.Linear(cfg.n_embd, cfg.n_embd, bias=False)
    self.W2 = torch.nn.Linear(cfg.n_embd, cfg.n_embd, bias=False)
    self.W3 = torch.nn.Linear(cfg.n_embd, cfg.n_embd, bias=False)
    self.W4 = torch.nn.Linear(cfg.n_embd, cfg.n_embd, bias=False)
