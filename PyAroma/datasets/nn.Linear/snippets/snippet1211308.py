from transformers import *
from transformers.models.distilbert.modeling_distilbert import *
import math
import torch
from torch import nn as nn


def __init__(self, config):
    super().__init__(config)
    self.transformer = SplitTransformer(config)
    self.embeddings = PosOffsetEmbeddings(config)
    self._classification_layer = torch.nn.Linear(self.config.hidden_size, 1, bias=False)
    self.join_layer_idx = config.join_layer_idx
