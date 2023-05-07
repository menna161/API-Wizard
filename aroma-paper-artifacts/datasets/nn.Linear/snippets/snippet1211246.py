from typing import Dict, Union
import torch
from torch import nn as nn
from transformers import PreTrainedModel, PretrainedConfig
from transformers import AutoModel
import math


def __init__(self, cfg) -> None:
    super().__init__(cfg)
    self.return_vecs = cfg.return_vecs
    self.bert_model = AutoModel.from_pretrained(cfg.bert_model)
    for p in self.bert_model.parameters():
        p.requires_grad = cfg.trainable
    self._dropout = torch.nn.Dropout(p=cfg.dropout)
    self.compressor = torch.nn.Linear(self.bert_model.config.hidden_size, cfg.compression_dim)
