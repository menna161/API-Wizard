import torch
import torch.nn as nn
import torch.nn.functional as F
from fairseq import utils
from fairseq.models import FairseqDecoder, FairseqLanguageModel, register_model, register_model_architecture
from fairseq.modules import LayerNorm, TransformerSentenceEncoder
from fairseq.modules.transformer_sentence_encoder import init_bert_params
from .hub_interface import McbertHubInterface
from fairseq import hub_utils


def __init__(self, input_dim, inner_dim, num_classes, activation_fn, pooler_dropout):
    super().__init__()
    self.dense = nn.Linear(input_dim, inner_dim)
    self.activation_fn = utils.get_activation_fn(activation_fn)
    self.dropout = nn.Dropout(p=pooler_dropout)
    self.out_proj = nn.Linear(inner_dim, num_classes)
