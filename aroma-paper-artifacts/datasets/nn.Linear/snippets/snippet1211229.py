from typing import Dict, Union
import torch
from transformers import AutoModel
from transformers import PreTrainedModel, PretrainedConfig


def __init__(self, cfg) -> None:
    super().__init__(cfg)
    self.bert_model = AutoModel.from_pretrained(cfg.bert_model)
    for p in self.bert_model.parameters():
        p.requires_grad = cfg.trainable
    self.use_compressor = (cfg.compress_dim > (- 1))
    if self.use_compressor:
        self.compressor = torch.nn.Linear(self.bert_model.config.hidden_size, cfg.compress_dim)
    self.return_vecs = cfg.return_vecs
