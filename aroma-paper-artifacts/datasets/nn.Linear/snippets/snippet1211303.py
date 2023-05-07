from matchmaker.losses.lambdarank import LambdaLoss
from matchmaker.losses.soft_crossentropy import SoftCrossEntropy
from typing import Dict, Union
import torch
from torch import nn as nn
from transformers import AutoModel


def __init__(self, bert_model: Union[(str, AutoModel)], dropout: float=0.0, trainable: bool=True, parade_aggregate_layers=2, parade_aggregate_type='tf', chunk_size=50, overlap=7, padding_idx: int=0) -> None:
    super().__init__()
    if isinstance(bert_model, str):
        self.bert_model = AutoModel.from_pretrained(bert_model)
    else:
        self.bert_model = bert_model
    for p in self.bert_model.parameters():
        p.requires_grad = trainable
    self._dropout = torch.nn.Dropout(p=dropout)
    self.padding_idx = padding_idx
    self.chunk_size = chunk_size
    self.overlap = overlap
    self.extended_chunk_size = (self.chunk_size + (2 * self.overlap))
    self.parade_aggregate_type = parade_aggregate_type
    if (parade_aggregate_type == 'tf'):
        encoder_layer = nn.TransformerEncoderLayer(self.bert_model.config.dim, self.bert_model.config.num_attention_heads, dim_feedforward=self.bert_model.config.hidden_dim, dropout=self.bert_model.config.dropout)
        self.parade_aggregate_tf = nn.TransformerEncoder(encoder_layer, parade_aggregate_layers, norm=None)
    self.score_reduction = nn.Linear(self.bert_model.config.dim, 1)
