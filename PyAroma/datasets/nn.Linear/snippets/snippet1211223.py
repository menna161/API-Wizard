from typing import Dict, Union
import torch
from torch import nn as nn
from transformers import AutoModel
from transformers import PreTrainedModel, PretrainedConfig


def __init__(self, cfg) -> None:
    super().__init__(cfg)
    self.bert_model = AutoModel.from_pretrained(cfg.bert_model)
    for p in self.bert_model.parameters():
        p.requires_grad = cfg.trainable
    self._classification_layer = torch.nn.Linear(self.bert_model.config.hidden_size, 1)
