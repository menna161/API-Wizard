from matchmaker.losses.lambdarank import LambdaLoss
from matchmaker.losses.soft_crossentropy import SoftCrossEntropy
from typing import Dict, Union
import torch
from torch import nn as nn
from transformers import AutoModel
from transformers import PreTrainedModel, PretrainedConfig


def __init__(self, bert_model: Union[(str, AutoModel)], dropout: float=0.0, trainable: bool=True, sample_train_type='lambdaloss', sample_n=1, sample_context='ck', top_k_chunks=3, chunk_size=50, overlap=7, padding_idx: int=0) -> None:
    super().__init__()
    if isinstance(bert_model, str):
        self.bert_model = AutoModel.from_pretrained(bert_model)
    else:
        self.bert_model = bert_model
    for p in self.bert_model.parameters():
        p.requires_grad = trainable
    self._classification_layer = torch.nn.Linear(self.bert_model.config.hidden_size, 1)
    self.top_k_chunks = top_k_chunks
    self.top_k_scoring = nn.Parameter(torch.full([1, self.top_k_chunks], 1, dtype=torch.float32, requires_grad=True))
    self.padding_idx = padding_idx
    self.chunk_size = chunk_size
    self.overlap = overlap
    self.extended_chunk_size = (self.chunk_size + (2 * self.overlap))
    self.sample_train_type = sample_train_type
    self.sample_n = sample_n
    self.sample_context = sample_context
    if (self.sample_context == 'ck'):
        i = 3
        self.sample_cnn3 = nn.Sequential(nn.ConstantPad1d((0, (i - 1)), 0), nn.Conv1d(kernel_size=i, in_channels=self.bert_model.config.dim, out_channels=self.bert_model.config.dim), nn.ReLU())
    elif (self.sample_context == 'ck-small'):
        i = 3
        self.sample_projector = nn.Linear(self.bert_model.config.dim, 384)
        self.sample_cnn3 = nn.Sequential(nn.ConstantPad1d((0, (i - 1)), 0), nn.Conv1d(kernel_size=i, in_channels=384, out_channels=128), nn.ReLU())
    elif (self.sample_context == 'tk'):
        self.tk_projector = nn.Linear(self.bert_model.config.dim, 384)
        encoder_layer = nn.TransformerEncoderLayer(384, 8, dim_feedforward=384, dropout=0)
        self.tk_contextualizer = nn.TransformerEncoder(encoder_layer, 1, norm=None)
        self.tK_mixer = nn.Parameter(torch.full([1], 0.5, dtype=torch.float32, requires_grad=True))
    self.sampling_binweights = nn.Linear(11, 1, bias=True)
    torch.nn.init.uniform_(self.sampling_binweights.weight, (- 0.01), 0.01)
    self.kernel_alpha_scaler = nn.Parameter(torch.full([1, 1, 11], 1, dtype=torch.float32, requires_grad=True))
    self.register_buffer('mu', nn.Parameter(torch.tensor([1.0, 0.9, 0.7, 0.5, 0.3, 0.1, (- 0.1), (- 0.3), (- 0.5), (- 0.7), (- 0.9)]), requires_grad=False).view(1, 1, 1, (- 1)))
    self.register_buffer('sigma', nn.Parameter(torch.tensor([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]), requires_grad=False).view(1, 1, 1, (- 1)))
